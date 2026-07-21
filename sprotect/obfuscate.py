"""AST-based obfuscation engine."""

from __future__ import annotations
import ast, base64, struct, hashlib, secrets
from sprotect.types import ObfuscateConfig
from sprotect.random_gen import NameGen

def collect_defs(source: str, cfg: ObfuscateConfig, mapping: dict[str, str]) -> None:
    reserved = set(cfg.rename_rules.reserved or [])
    gen = NameGen(cfg.rename_rules.style, cfg.rename_rules.dictionary)
    try:
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name not in reserved and not node.name.startswith("__"):
                    mapping.setdefault(node.name, gen.gen())
            elif isinstance(node, ast.ClassDef):
                if node.name not in reserved and not node.name.startswith("__"):
                    mapping.setdefault(node.name, gen.gen())
            elif isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id not in reserved and not t.id.startswith("__"):
                        mapping.setdefault(t.id, gen.gen())
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id not in reserved and not node.target.id.startswith("__"):
                    mapping.setdefault(node.target.id, gen.gen())
    except SyntaxError: pass


def _opaque_predicate() -> ast.If:
    """Generate an opaque predicate: a condition that always takes one branch
    but looks complex to static analysis.
    Uses an always-true XOR comparison."""
    import random
    x = random.randint(1, 1000000)
    test = ast.Compare(
        left=ast.BinOp(
            left=ast.BinOp(left=ast.Constant(x), op=ast.BitXor(), right=ast.Constant(x)),
            op=ast.Add(), right=ast.Constant(1)),
        ops=[ast.Eq()],
        comparators=[ast.Constant(1)])
    return ast.If(test=test, body=[ast.Pass()], orelse=[])


def _split_string(s: str, n: int = 3) -> ast.Call:
    """Split a string into n fragments and reconstruct at runtime with +."""
    if len(s) <= n:
        return ast.Constant(s)
    pieces = []
    chunk = max(1, len(s) // n)
    for i in range(0, len(s), chunk):
        pieces.append(ast.Constant(s[i:i+chunk]))
    expr = pieces[0]
    for p in pieces[1:]:
        expr = ast.BinOp(left=expr, op=ast.Add(), right=p)
    return expr


class Obfuscator(ast.NodeTransformer):
    def __init__(self, cfg: ObfuscateConfig, mapping: dict[str, str] | None = None):
        self.cfg = cfg
        self.map = mapping if mapping is not None else {}
        self.reserved = set(cfg.rename_rules.reserved or [])
        self.gen = NameGen(cfg.rename_rules.style, cfg.rename_rules.dictionary)
        self._class_depth = 0; self._fstring_depth = 0; self._params: list[set[str]] = []
        self._dead_count = 0

    def _name(self, old: str) -> str:
        if old.startswith("__") or old in self.reserved: return old
        self.map.setdefault(old, self.gen.gen())
        return self.map[old]

    def _push_params(self, node):
        ps = set()
        for a in node.args.args + node.args.posonlyargs + node.args.kwonlyargs: ps.add(a.arg)
        if node.args.vararg: ps.add(node.args.vararg.arg)
        if node.args.kwarg: ps.add(node.args.kwarg.arg)
        self._params.append(ps)
    def _pop_params(self): self._params.pop()
    def _is_param(self, n: str) -> bool: return any(n in s for s in self._params)

    def obfuscate(self, src: str) -> str:
        tree = ast.parse(src)
        self._collect(tree)
        tree = self.visit(tree)
        if self.cfg.encrypt_strings or self.cfg.encrypt_numbers:
            tree = _LiteralEncryptor(self.cfg, self._fstring_depth).visit(tree)
        if self.cfg.dead_code_injection:
            self._inject_dead_code(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def _collect(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._name(node.name)
            elif isinstance(node, ast.ClassDef):
                self._name(node.name)

    def _inject_dead_code(self, tree):
        """Insert opaque predicates + dead code into function bodies."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if len(node.body) > 1 and self._dead_count % 2 == 0:
                    node.body.insert(0, _opaque_predicate())
                self._dead_count += 1

    def visit_alias(self, node: ast.alias):
        if node.name in self.map: node.name = self.map[node.name]
        return node

    def visit_Lambda(self, node: ast.Lambda):
        self._push_params(node); node = self.generic_visit(node); self._pop_params(); return node

    def visit_Name(self, node: ast.Name):
        if node.id in self.map and not self._is_param(node.id):
            node.id = self.map[node.id]
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self.cfg.rename_functions and self._class_depth == 0: node.name = self._name(node.name)
        self._push_params(node); self.generic_visit(node); self._pop_params(); return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if self.cfg.rename_functions and self._class_depth == 0: node.name = self._name(node.name)
        self._push_params(node); self.generic_visit(node); self._pop_params(); return node

    def visit_ClassDef(self, node: ast.ClassDef):
        if self.cfg.rename_classes: node.name = self._name(node.name)
        self._class_depth += 1; self.generic_visit(node); self._class_depth -= 1; return node

    def visit_Nonlocal(self, node: ast.Nonlocal):
        node.names = [self.map.get(n, n) for n in node.names]
        return node

    def visit_Global(self, node: ast.Global):
        node.names = [self.map.get(n, n) for n in node.names]
        return node

    def visit_arg(self, node: ast.arg): return node
    def visit_FormattedValue(self, n):
        self._fstring_depth += 1; r = self.generic_visit(n); self._fstring_depth -= 1; return r
    def visit_JoinedStr(self, n):
        self._fstring_depth += 1; r = self.generic_visit(n); self._fstring_depth -= 1; return r


class _LiteralEncryptor(ast.NodeTransformer):
    def __init__(self, cfg: ObfuscateConfig, fdepth=0): self.cfg = cfg; self._fdepth = fdepth
    def visit_FormattedValue(self, n): self._fdepth += 1; r = self.generic_visit(n); self._fdepth -= 1; return r
    def visit_JoinedStr(self, n): self._fdepth += 1; r = self.generic_visit(n); self._fdepth -= 1; return r

    def visit_Constant(self, node):
        if isinstance(node.value, str) and self.cfg.encrypt_strings and len(node.value) > 1 and self._fdepth == 0:
            e = base64.b64encode(node.value.encode()).decode()
            return ast.Call(func=ast.Attribute(value=ast.Call(func=ast.Attribute(
                value=ast.Call(func=ast.Name(id="__import__"), args=[ast.Constant("base64")], keywords=[]),
                attr="b64decode"), args=[ast.Constant(e)], keywords=[]), attr="decode"), args=[], keywords=[])
        if isinstance(node.value, (int,float)) and not isinstance(node.value, bool) and self.cfg.encrypt_numbers:
            fmt = "i" if isinstance(node.value, int) and -2**31 <= node.value < 2**31 else "q" if isinstance(node.value, int) else "d"
            e = base64.b64encode(struct.pack(fmt, node.value)).decode()
            return ast.Subscript(value=ast.Call(func=ast.Attribute(
                value=ast.Call(func=ast.Name(id="__import__"), args=[ast.Constant("struct")], keywords=[]),
                attr="unpack"), args=[ast.Constant(fmt), ast.Call(func=ast.Attribute(
                value=ast.Call(func=ast.Name(id="__import__"), args=[ast.Constant("base64")], keywords=[]),
                attr="b64decode"), args=[ast.Constant(e)], keywords=[])], keywords=[]), slice=ast.Constant(0), ctx=ast.Load())
        return node
