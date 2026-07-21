"""AST-based obfuscation engine."""

from __future__ import annotations
import ast, base64, struct, hashlib, secrets
from sprotect.types import ObfuscateConfig
from sprotect.random_gen import NameGen

def collect_defs(source: str, cfg: ObfuscateConfig, mapping: dict[str, str],
                 param_names: set[str] | None = None) -> None:
    reserved = set(cfg.rename_rules.reserved or [])
    gen = NameGen(cfg.rename_rules.style, cfg.rename_rules.dictionary)
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name not in reserved and not node.name.startswith("_"):
                    mapping.setdefault(node.name, gen.gen())
                for arg in node.args.args + node.args.kwonlyargs + node.args.posonlyargs:
                    if param_names is not None: param_names.add(arg.arg)
                if node.args.vararg and param_names is not None: param_names.add(node.args.vararg.arg)
                if node.args.kwarg and param_names is not None: param_names.add(node.args.kwarg.arg)
            elif isinstance(node, ast.ClassDef):
                if node.name not in reserved and not node.name.startswith("_"):
                    mapping.setdefault(node.name, gen.gen())
            elif isinstance(node, ast.ExceptHandler) and node.name and param_names is not None:
                param_names.add(node.name)
            elif cfg.rename_variables and isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id not in reserved and not t.id.startswith("_") and t.id not in (param_names or set()):
                        mapping.setdefault(t.id, gen.gen())
            elif cfg.rename_variables and isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id not in reserved and not node.target.id.startswith("_") and node.target.id not in (param_names or set()):
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
    def __init__(self, cfg: ObfuscateConfig, mapping: dict[str, str] | None = None,
                 param_names: set[str] | None = None):
        self.cfg = cfg
        self.map = mapping if mapping is not None else {}
        self.param_names = param_names or set()
        self.reserved = set(cfg.rename_rules.reserved or [])
        self.gen = NameGen(cfg.rename_rules.style, cfg.rename_rules.dictionary)
        self._class_depth = 0; self._fstring_depth = 0; self._params: list[set[str]] = []
        self._dead_count = 0
        # Feature detection flags for protected patterns
        self._in_dataclass = False
        self._in_enum = False
        self._protected_names: set[str] = set()
        self._class_names: set[str] = set()

    _BUILTIN_RESERVED = frozenset({
        "property", "staticmethod", "classmethod", "setter", "deleter",
        "getter", "__init__", "__new__", "__call__",
    })

    def _name(self, old: str) -> str:
        if old.startswith("_") or old in self.reserved or old in self._BUILTIN_RESERVED: return old
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
        if self.cfg.obfuscate_imports:
            tree = _ImportObfuscator().visit(tree)
        if self.cfg.obfuscate_arithmetic:
            tree = _ArithmeticObfuscator().visit(tree)
        if self.cfg.obfuscate_booleans:
            tree = _BooleanObfuscator().visit(tree)
        if self.cfg.encrypt_strings or self.cfg.encrypt_numbers:
            tree = _LiteralEncryptor(self.cfg, self._fstring_depth).visit(tree)
        if self.cfg.obfuscate_calls:
            tree = _CallObfuscator().visit(tree)
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

    def _has_decorator(self, node: ast.ClassDef | ast.FunctionDef, name: str) -> bool:
        for d in node.decorator_list:
            if isinstance(d, ast.Name) and d.id == name: return True
            if isinstance(d, ast.Attribute) and d.attr == name: return True
            if isinstance(d, ast.Call):
                fn = d.func
                if isinstance(fn, ast.Name) and fn.id == name: return True
                if isinstance(fn, ast.Attribute) and fn.attr == name: return True
        return False

    def _has_base(self, node: ast.ClassDef, name: str) -> bool:
        for b in node.bases:
            if isinstance(b, ast.Attribute) and b.attr == name: return True
            if isinstance(b, ast.Name) and b.id == name: return True
        return False

    def visit_alias(self, node: ast.alias):
        if self.cfg.rename_variables and node.name in self.map:
            node.name = self.map[node.name]
        return node

    def visit_Lambda(self, node: ast.Lambda):
        self._push_params(node); node = self.generic_visit(node); self._pop_params(); return node

    def visit_Name(self, node: ast.Name):
        if (self._in_dataclass or self._in_enum) and isinstance(node.ctx, ast.Store):
            self._protected_names.add(node.id)
        if (self.cfg.rename_variables and node.id in self.map
            and not self._is_param(node.id) and node.id not in self.param_names
            and node.id not in self._protected_names
            and node.id not in self._BUILTIN_RESERVED
            and node.id not in self._class_names):
            node.id = self.map[node.id]
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self.cfg.rename_functions and self._class_depth == 0: node.name = self._name(node.name)
        self._push_params(node); self.generic_visit(node); self._pop_params(); return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if self.cfg.rename_functions and self._class_depth == 0: node.name = self._name(node.name)
        self._push_params(node); self.generic_visit(node); self._pop_params(); return node

    def _collect_class_names(self, node: ast.ClassDef) -> set[str]:
        """Collect names defined directly in a class (methods, attributes)."""
        names: set[str] = set()
        for child in ast.walk(node):
            if child is node: continue
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                names.add(child.name)
            elif isinstance(child, ast.ClassDef):
                names.add(child.name)
        return names

    def visit_ClassDef(self, node: ast.ClassDef):
        if self.cfg.rename_classes: node.name = self._name(node.name)
        prev_dc, prev_enum = self._in_dataclass, self._in_enum
        self._in_dataclass = self._has_decorator(node, "dataclass")
        self._in_enum = any(
            isinstance(b, (ast.Name, ast.Attribute))
            and (b.id if isinstance(b, ast.Name) else b.attr) in ("Enum", "IntEnum", "StrEnum", "IntFlag", "Flag")
            for b in node.bases
        )
        self._class_names = self._collect_class_names(node)
        protected_before = set(self._protected_names)
        self._class_depth += 1; self.generic_visit(node); self._class_depth -= 1
        if self._in_dataclass or self._in_enum:
            protected_now = self._protected_names - protected_before
            for pn in protected_now:
                self.map.pop(pn, None)
        self._in_dataclass, self._in_enum = prev_dc, prev_enum
        return node

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.name and node.name in self.map:
            node.name = self.map[node.name]
        return self.generic_visit(node)

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


class _ImportObfuscator(ast.NodeTransformer):
    """Transform import statements into __import__() calls."""

    def visit_Import(self, node: ast.Import):
        new_nodes: list[ast.AST] = []
        for alias in node.names:
            parts = alias.name.split(".")
            imp = ast.Call(func=ast.Name(id="__import__"), args=[ast.Constant(alias.name)], keywords=[])
            if alias.asname:
                val = imp
                for p in parts[1:]:
                    val = ast.Attribute(value=val, attr=p, ctx=ast.Load())
                new_nodes.append(ast.Assign(targets=[ast.Name(id=alias.asname, ctx=ast.Store())], value=val))
            else:
                new_nodes.append(ast.Assign(targets=[ast.Name(id=parts[0], ctx=ast.Store())], value=imp))
        return new_nodes if len(new_nodes) != 1 else new_nodes[0]

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if not node.module:
            return node
        names_list = ast.List(elts=[ast.Constant(a.name) for a in node.names], ctx=ast.Load())
        base = ast.Call(
            func=ast.Name(id="__import__"),
            args=[ast.Constant(node.module)],
            keywords=[ast.keyword(arg="fromlist", value=names_list)])
        new_nodes: list[ast.AST] = []
        for alias in node.names:
            attr = ast.Attribute(value=base, attr=alias.name, ctx=ast.Load())
            target = alias.asname or alias.name
            new_nodes.append(ast.Assign(targets=[ast.Name(id=target, ctx=ast.Store())], value=attr))
        return new_nodes if len(new_nodes) != 1 else new_nodes[0]


class _CallObfuscator(ast.NodeTransformer):
    """Wrap function calls in lambda wrappers."""

    def visit_Call(self, node: ast.Call):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id in ("__import__", "exec", "eval", "compile", "getattr", "hasattr"):
            return node
        if isinstance(node.func, ast.Attribute):
            return node
        if len(node.args) <= 2 and not node.keywords and secrets.randbelow(4) == 0:
            arg_names = [f"_a{i}" for i in range(len(node.args))]
            lambda_args = ast.arguments(
                args=[ast.arg(arg=n) for n in arg_names],
                posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[])
            inner_call = ast.Call(func=node.func,
                args=[ast.Name(id=n, ctx=ast.Load()) for n in arg_names],
                keywords=[])
            lambda_node = ast.Lambda(args=lambda_args, body=inner_call)
            return ast.Call(func=lambda_node,
                args=node.args, keywords=[])
        return node


class _ArithmeticObfuscator(ast.NodeTransformer):
    """Obfuscate arithmetic expressions: a+b → a-(-b), a*2 → a<<1, etc."""

    def visit_BinOp(self, node: ast.BinOp):
        self.generic_visit(node)
        if isinstance(node.op, ast.Add) and secrets.randbelow(3) == 0:
            neg = ast.UnaryOp(op=ast.USub(), operand=node.right)
            return ast.BinOp(left=node.left, op=ast.Sub(), right=neg)
        if isinstance(node.op, ast.Sub) and secrets.randbelow(3) == 0:
            neg = ast.UnaryOp(op=ast.USub(), operand=node.right)
            return ast.BinOp(left=node.left, op=ast.Add(), right=neg)
        if isinstance(node.op, ast.Mult) and isinstance(node.right, ast.Constant) and isinstance(node.right.value, int):
            v = node.right.value
            if v > 0 and (v & (v - 1)) == 0 and secrets.randbelow(2) == 0:
                shift = v.bit_length() - 1
                return ast.BinOp(left=node.left, op=ast.LShift(), right=ast.Constant(shift))
        return node


class _BooleanObfuscator(ast.NodeTransformer):
    """Transform True/False into expressions like 1==1/1!=1."""

    def visit_Constant(self, node: ast.Constant):
        if node.value is True and secrets.randbelow(2) == 0:
            return ast.Compare(
                left=ast.Constant(secrets.randbelow(1000)),
                ops=[ast.Eq()],
                comparators=[ast.Constant(secrets.randbelow(1000))])
        if node.value is False and secrets.randbelow(2) == 0:
            return ast.Compare(
                left=ast.Constant(secrets.randbelow(1000)),
                ops=[ast.NotEq()],
                comparators=[ast.Constant(secrets.randbelow(1000))])
        return node


class _LiteralEncryptor(ast.NodeTransformer):
    def __init__(self, cfg: ObfuscateConfig, fdepth=0): self.cfg = cfg; self._fdepth = fdepth
    def visit_FormattedValue(self, n): self._fdepth += 1; r = self.generic_visit(n); self._fdepth -= 1; return r
    def visit_JoinedStr(self, n): self._fdepth += 1; r = self.generic_visit(n); self._fdepth -= 1; return r

    def visit_Constant(self, node):
        if isinstance(node.value, str) and self.cfg.encrypt_strings and len(node.value) > 1 and self._fdepth == 0:
            if self.cfg.string_split and secrets.randbelow(2) == 0:
                return _split_string(node.value, secrets.randbelow(3) + 2)
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
