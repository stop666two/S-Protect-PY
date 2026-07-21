"""AST-based obfuscation engine."""

from __future__ import annotations
import ast, base64, struct
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
    except SyntaxError: pass

class Obfuscator(ast.NodeTransformer):
    def __init__(self, cfg: ObfuscateConfig, mapping: dict[str, str] | None = None):
        self.cfg = cfg
        self.map = mapping if mapping is not None else {}
        self.reserved = set(cfg.rename_rules.reserved or [])
        self.gen = NameGen(cfg.rename_rules.style, cfg.rename_rules.dictionary)
        self._class_depth = 0; self._fstring_depth = 0; self._params: list[set[str]] = []

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
            tree = _LiteralEncryptor(self.cfg).visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def _collect(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._name(node.name)
            elif isinstance(node, ast.ClassDef):
                self._name(node.name)

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

    def visit_arg(self, node: ast.arg): return node

    def visit_FormattedValue(self, node):
        self._fstring_depth += 1; r = self.generic_visit(node); self._fstring_depth -= 1; return r

    def visit_JoinedStr(self, node):
        self._fstring_depth += 1; r = self.generic_visit(node); self._fstring_depth -= 1; return r


class _LiteralEncryptor(ast.NodeTransformer):
    def __init__(self, cfg: ObfuscateConfig): self.cfg = cfg; self._fdepth = 0

    def visit_FormattedValue(self, n):
        self._fdepth += 1; r = self.generic_visit(n); self._fdepth -= 1; return r
    def visit_JoinedStr(self, n):
        self._fdepth += 1; r = self.generic_visit(n); self._fdepth -= 1; return r

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
