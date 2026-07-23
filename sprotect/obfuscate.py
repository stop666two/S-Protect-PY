# OBFUSCATION ENGINE: AST-level code transformation
# PASSES: 8 transformer stages

"""AST-based obfuscation engine."""

from __future__ import annotations
import ast, base64, struct, hashlib, secrets
from sprotect.types import ObfuscateConfig
from sprotect.random_gen import NameGen


def collect_defs(source: str, cfg: ObfuscateConfig, mapping: dict[str, str],
                 param_names: set[str] | None = None,
                 import_names: set[str] | None = None) -> None:
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
            if import_names is not None:
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_names.add(alias.asname or alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        import_names.add(node.module.split(".")[0])
                    for alias in node.names:
                        import_names.add(alias.asname or alias.name)
    except SyntaxError: pass


def _synthesize_opaque_check() -> ast.If:
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
    result = ast.If(test=test, body=[ast.Pass()], orelse=[])
    ast.fix_missing_locations(result)
    return result


def _fragment_string_ast(s: str, n: int = 3) -> ast.Call:
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
                 param_names: set[str] | None = None,
                 import_names: set[str] | None = None):
        self.cfg = cfg
        self.map = mapping if mapping is not None else {}
        self._param_set = param_names or set()
        self._import_set = import_names or set()
        self.reserved = set(cfg.rename_rules.reserved or [])
        self.gen = NameGen(cfg.rename_rules.style, cfg.rename_rules.dictionary)
        self._cls_nesting = 0; self._fmt_nesting = 0; self._param_stack: list[set[str]] = []
        self._dead_counter = 0
        # Feature detection flags for protected patterns
        self._within_dataclass = False
        self._within_enum = False
        self._guarded_names: set[str] = set()
        self._cls_defs: set[str] = set()

    _RESERVED_BUILTINS = frozenset({
        "property", "staticmethod", "classmethod", "setter", "deleter",
        "getter", "__init__", "__new__", "__call__",
    })

    def _name(self, old: str) -> str:
        if old.startswith("_") or old in self.reserved or old in self._RESERVED_BUILTINS: return old
        self.map.setdefault(old, self.gen.gen())
        return self.map[old]

    def _push_params(self, node):
        ps = set()
        for a in node.args.args + node.args.posonlyargs + node.args.kwonlyargs: ps.add(a.arg)
        if node.args.vararg: ps.add(node.args.vararg.arg)
        if node.args.kwarg: ps.add(node.args.kwarg.arg)
        self._param_stack.append(ps)
    def _pop_params(self): self._param_stack.pop()
    def _is_param(self, n: str) -> bool: return any(n in s for s in self._param_stack)

    def obfuscate(self, src: str) -> str:
        tree = ast.parse(src)
        self._pre_scan_names(tree)
        tree = self.visit(tree)
        if self.map:
            tree = _AttrObfuscator(self.map, self._param_set, self._import_set).visit(tree)
        if self.cfg.obfuscate_imports:
            tree = _ImportObfuscator(self.map).visit(tree)
        if self.cfg.obfuscate_arithmetic:
            tree = _ArithmeticObfuscator().visit(tree)
        if self.cfg.obfuscate_booleans:
            tree = _BooleanObfuscator().visit(tree)
        if self.cfg.encrypt_strings or self.cfg.encrypt_numbers:
            tree = _LiteralEncryptor(self.cfg, self._fmt_nesting).visit(tree)
        if self.cfg.obfuscate_calls:
            tree = _CallObfuscator().visit(tree)
        if self.cfg.control_flow_flattening:
            if secrets.randbelow(2):
                tree = _MatchCaseFlattener().visit(tree)
            else:
                tree = _ControlFlowFlattener().visit(tree)
        if self.cfg.dead_code_injection:
            self._seed_dead_blocks(tree)
            tree = _HoneypotInjector(self.map).visit(tree)
        tree = _ImplicitFlowInjector().visit(tree)
        if self.cfg.encrypt_strings:
            tree = _StringDisperser().visit(tree)
        if self.cfg.obfuscate_arithmetic:
            tree = _OpaqueExprInjector().visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def _pre_scan_names(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._name(node.name)
            elif isinstance(node, ast.ClassDef):
                self._name(node.name)

    def _seed_dead_blocks(self, tree):
        """Insert opaque predicates + dead code into function bodies."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if len(node.body) > 1 and self._dead_counter % 2 == 0:
                    node.body.insert(0, _synthesize_opaque_check())
                self._dead_counter += 1

    def _check_decorator(self, node: ast.ClassDef | ast.FunctionDef, name: str) -> bool:
        for d in node.decorator_list:
            if isinstance(d, ast.Name) and d.id == name: return True
            if isinstance(d, ast.Attribute) and d.attr == name: return True
            if isinstance(d, ast.Call):
                fn = d.func
                if isinstance(fn, ast.Name) and fn.id == name: return True
                if isinstance(fn, ast.Attribute) and fn.attr == name: return True
        return False

    def _check_base_class(self, node: ast.ClassDef, name: str) -> bool:
        for b in node.bases:
            if isinstance(b, ast.Attribute) and b.attr == name: return True
            if isinstance(b, ast.Name) and b.id == name: return True
        return False

    def visit_alias(self, node: ast.alias):
        if node.name in self.map and not node.name.startswith("_"):
            new = self.map.get(node.name)
            if new:
                node.name = new
        return node

    def visit_Lambda(self, node: ast.Lambda):
        self._push_params(node); node = self.generic_visit(node); self._pop_params(); return node

    def visit_Name(self, node: ast.Name):
        if (self._within_dataclass or self._within_enum) and isinstance(node.ctx, ast.Store):
            self._guarded_names.add(node.id)
        if (node.id in self.map
            and not self._is_param(node.id) and node.id not in self._param_set
            and node.id not in self._guarded_names
            and node.id not in self._RESERVED_BUILTINS
            and node.id not in self._cls_defs
            and not node.id.startswith("_")):
            node.id = self.map[node.id]
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self.cfg.rename_functions and self._cls_nesting == 0: node.name = self._name(node.name)
        self._push_params(node); self.generic_visit(node); self._pop_params(); return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if self.cfg.rename_functions and self._cls_nesting == 0: node.name = self._name(node.name)
        self._push_params(node); self.generic_visit(node); self._pop_params(); return node

    def _gather_class_members(self, node: ast.ClassDef) -> set[str]:
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
        prev_dc, prev_enum = self._within_dataclass, self._within_enum
        self._within_dataclass = self._check_decorator(node, "dataclass")
        self._within_enum = any(
            isinstance(b, (ast.Name, ast.Attribute))
            and (b.id if isinstance(b, ast.Name) else b.attr) in ("Enum", "IntEnum", "StrEnum", "IntFlag", "Flag")
            for b in node.bases
        )
        self._cls_defs = self._gather_class_members(node)
        protected_before = set(self._guarded_names)
        self._cls_nesting += 1; self.generic_visit(node); self._cls_nesting -= 1
        if self._within_dataclass or self._within_enum:
            protected_now = self._guarded_names - protected_before
            for pn in protected_now:
                self.map.pop(pn, None)
        self._within_dataclass, self._within_enum = prev_dc, prev_enum
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
        self._fmt_nesting += 1; r = self.generic_visit(n); self._fmt_nesting -= 1; return r
    def visit_JoinedStr(self, n):
        self._fmt_nesting += 1; r = self.generic_visit(n); self._fmt_nesting -= 1; return r


class _AttrObfuscator(ast.NodeTransformer):
    """Rename attribute access (obj.ATTR). Only renames when the object
    itself is a renamed project variable — stdlib/third-party types are safe."""

    def __init__(self, rename_map: dict[str, str], param_names: set[str],
                 import_names: set[str]):
        self._rename_table = rename_map
        self._param_set = param_names
        self._import_set = import_names

    def visit_Attribute(self, node: ast.Attribute):
        self.generic_visit(node)
        if (node.attr in self._rename_table and isinstance(node.value, ast.Name)
                and node.value.id in self._rename_table):
            if node.value.id in self._param_set:
                return node
            if node.value.id in self._import_set and node.attr not in self._rename_table:
                return node
            node.attr = self._rename_table[node.attr]
        return node


class _ImportObfuscator(ast.NodeTransformer):
    """Transform import statements into __import__() calls."""

    def __init__(self, rename_map: dict[str, str] | None = None):
        self._rename_table = rename_map or {}

    def _resolve_name(self, name: str) -> str:
        return self._rename_table.get(name, name)

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
            target = self._resolve_name(alias.asname or alias.name)
            new_nodes.append(ast.Assign(targets=[ast.Name(id=target, ctx=ast.Store())], value=attr))
        return new_nodes if len(new_nodes) != 1 else new_nodes[0]


class _CallObfuscator(ast.NodeTransformer):
    """Wrap function calls in lambda wrappers to break static analysis."""

    def visit_Call(self, node: ast.Call):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id in ("__import__", "exec", "eval", "compile", "getattr", "hasattr"):
            return node
        if any(isinstance(a, ast.Starred) for a in node.args):
            return node
        if len(node.args) <= 3 and not node.keywords and secrets.randbelow(3) == 0:
            if isinstance(node.func, ast.Attribute):
                arg_count = 1 + len(node.args)
                arg_names = [f"_a{i}" for i in range(arg_count)]
                inner_call = ast.Call(
                    func=ast.Attribute(value=ast.Name(id=arg_names[0], ctx=ast.Load()),
                                       attr=node.func.attr, ctx=ast.Load()),
                    args=[ast.Name(id=n, ctx=ast.Load()) for n in arg_names[1:]],
                    keywords=[])
                lambda_args = ast.arguments(
                    args=[ast.arg(arg=n) for n in arg_names],
                    posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[])
                return ast.Call(func=ast.Lambda(args=lambda_args, body=inner_call),
                    args=[node.func.value] + node.args, keywords=[])
            else:
                arg_count = 1 + len(node.args)
                arg_names = [f"_a{i}" for i in range(arg_count)]
                inner_call = ast.Call(func=ast.Name(id=arg_names[0], ctx=ast.Load()),
                    args=[ast.Name(id=n, ctx=ast.Load()) for n in arg_names[1:]],
                    keywords=[])
                lambda_args = ast.arguments(
                    args=[ast.arg(arg=n) for n in arg_names],
                    posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[])
                return ast.Call(func=ast.Lambda(args=lambda_args, body=inner_call),
                    args=[node.func] + node.args, keywords=[])
        return node


class _HoneypotInjector(ast.NodeTransformer):
    """Inject honeypot functions that look like real decrypt/validate logic."""

    _HONEYPOT_TEMPLATES = [
        'def {name}({args}):\n    import sys\n    while True:\n        pass\n    return None\n',
        'def {name}({args}):\n    import os\n    try:\n        os._exit(0)\n    except:\n        pass\n    return None\n',
        'def {name}({args}):\n    _d = bytearray(1024)\n    for i in range(1024):\n        _d[i] = (i * 7 + 3) & 0xFF\n    return bytes(_d)\n',
        'def {name}({args}):\n    import hashlib as _h\n    _k = _h.sha256(b"key").hexdigest()\n    _v = _h.md5(b"data").hexdigest()\n    return _k[:8] == _v[:8]\n',
        'def {name}({args}):\n    from cryptography.hazmat.primitives.ciphers import Cipher\n    from cryptography.hazmat.primitives.ciphers.algorithms import AES\n    from cryptography.hazmat.primitives.ciphers.modes import CBC\n    _c = Cipher(AES(b"k"*32), CBC(b"i"*16))\n    _d = _c.decryptor()\n    return _d.update(b"d"*16) + _d.finalize()\n',
        'def {name}({args}):\n    import hmac, hashlib\n    _k = hmac.new(b"key", b"data", hashlib.sha256).digest()\n    _v = hmac.new(b"key", b"expected", hashlib.sha256).digest()\n    return hmac.compare_digest(_k, _v)\n',
        'def {name}({args}):\n    from cryptography.hazmat.primitives.kdf.hkdf import HKDF\n    from cryptography.hazmat.primitives import hashes\n    _k = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"ctx").derive(b"ikm")\n    _t = b"test"\n    return bytes(a ^ b for a, b in zip(_k, _t * 4))\n',
    ]
    _HONEYPOT_ARGS = ["", "key, iv", "data, sig", "path, mode, ctx", "buf, offset",
                      "ciphertext, key, nonce", "encrypted, hmac_key", "payload, ctx, tag"]
    _HONEYPOT_ARGS = ["", "key, iv", "data, sig", "path, mode, ctx", "buf, offset"]

    def __init__(self, name_map: dict[str, str]):
        self._rename_table = name_map

    def visit_Module(self, node: ast.Module):
        self.generic_visit(node)
        used_names = set(self._rename_table.values())
        for _ in range(secrets.randbelow(3) + 2):
            fn = secrets.token_hex(5)
            while fn in used_names:
                fn = secrets.token_hex(5)
            used_names.add(fn)
            args = secrets.choice(self._HONEYPOT_ARGS)
            tpl = secrets.choice(self._HONEYPOT_TEMPLATES)
            trap_src = tpl.format(name=fn, args=args)
            try:
                trap_tree = ast.parse(trap_src)
                node.body.extend(trap_tree.body)
            except SyntaxError:
                pass
        return node


class _ControlFlowFlattener(ast.NodeTransformer):
    """Flatten control flow: convert sequential code to state machine."""

    def _has_yield(self, node: ast.AST) -> bool:
        for n in ast.walk(node):
            if isinstance(n, (ast.Yield, ast.YieldFrom, ast.GeneratorExp,
                              ast.ListComp, ast.SetComp, ast.DictComp,
                              ast.AsyncFunctionDef)):
                return True
        return False

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.generic_visit(node)
        if len(node.body) < 3 or self._has_yield(node):
            return node
        _state_var = f"_s{secrets.token_hex(2)}"
        _state_store = ast.Name(id=_state_var, ctx=ast.Store())
        _state_load = ast.Name(id=_state_var, ctx=ast.Load())
        blocks = list(enumerate(node.body))
        if len(blocks) < 3:
            return node
        if_chain = None
        for i, (_, stmt) in reversed(list(enumerate(blocks))):
            if i == len(blocks) - 1:
                if isinstance(stmt, ast.Return):
                    if_chain = [stmt]
                else:
                    if_chain = [stmt, ast.Break()]
            else:
                next_val = ast.BinOp(left=_state_load, op=ast.Add(), right=ast.Constant(1))
                if_chain = ast.If(
                    test=ast.Compare(left=_state_load, ops=[ast.Eq()], comparators=[ast.Constant(i)]),
                    body=[stmt, ast.Assign(targets=[_state_store], value=next_val)],
                    orelse=if_chain if isinstance(if_chain, list) else [if_chain])
        dispatch = ast.While(test=ast.Constant(True), body=[if_chain], orelse=[])
        node.body = [ast.Assign(targets=[_state_store], value=ast.Constant(0)), dispatch]
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return node


class _ImplicitFlowInjector(ast.NodeTransformer):
    """Hide constant values in control flow decisions instead of direct assignment.
    The real value is only reachable through one opaque branch; LLM data-flow
    analysis sees all branches and cannot determine which one executes."""

    def visit_Assign(self, node: ast.Assign):
        self.generic_visit(node)
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                v = node.value.value
                if not isinstance(v, bool) and secrets.randbelow(2):
                    _target = node.targets[0]
                    _bogus = v + secrets.randbelow(20) + 1 if isinstance(v, int) else v + 1.0
                    _x = secrets.randbelow(65536)
                    _pred = ast.Compare(
                        left=ast.BinOp(left=ast.Constant(_x), op=ast.BitXor(), right=ast.Constant(_x)),
                        ops=[ast.Eq()], comparators=[ast.Constant(0)])
                    _true_branch = ast.If(
                        test=_pred, body=[
                            ast.Assign(targets=[_target], value=ast.Constant(v))],
                        orelse=[
                            ast.Assign(targets=[_target], value=ast.Constant(_bogus))])
                    return _true_branch
        return node


class _MatchCaseFlattener(ast.NodeTransformer):
    """Flatten control flow using match/case dispatch instead of if/elif.
    LLMs struggle to statically analyze match/case with computed subject values."""

    def _has_yield(self, node: ast.AST) -> bool:
        for n in ast.walk(node):
            if isinstance(n, (ast.Yield, ast.YieldFrom, ast.GeneratorExp,
                              ast.ListComp, ast.SetComp, ast.DictComp,
                              ast.AsyncFunctionDef)):
                return True
        return False

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.generic_visit(node)
        if len(node.body) < 3 or self._has_yield(node):
            return node
        _sv = f"_m{secrets.token_hex(2)}"
        _store = ast.Name(id=_sv, ctx=ast.Store())
        _load = ast.Name(id=_sv, ctx=ast.Load())
        blocks = list(enumerate(node.body))
        if len(blocks) < 3:
            return node
        cases = []
        for i, stmt in blocks:
            if i == len(blocks) - 1:
                body = [stmt] if isinstance(stmt, ast.Return) else [stmt, ast.Break()]
            else:
                body = [stmt, ast.Assign(targets=[_store], value=ast.BinOp(left=_load, op=ast.Add(), right=ast.Constant(1)))]
            cases.append(ast.match_case(pattern=ast.MatchValue(value=ast.Constant(i)), guard=None, body=body))
        dispatch = ast.Match(subject=_load, cases=cases)
        loop = ast.While(test=ast.Constant(True), body=[dispatch], orelse=[])
        node.body = [ast.Assign(targets=[_store], value=ast.Constant(0)), loop]
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return node


class _ArithmeticObfuscator(ast.NodeTransformer):
    """Obfuscate arithmetic expressions: a+b → a-(-b), a*2 → a<<1, etc."""

    def _is_num(self, node: ast.AST) -> bool:
        return isinstance(node, ast.Constant) and isinstance(node.value, (int, float))

    def visit_BinOp(self, node: ast.BinOp):
        self.generic_visit(node)
        if isinstance(node.op, ast.Add) and self._is_num(node.left) and self._is_num(node.right) and secrets.randbelow(3) == 0:
            neg = ast.UnaryOp(op=ast.USub(), operand=node.right)
            return ast.BinOp(left=node.left, op=ast.Sub(), right=neg)
        if isinstance(node.op, ast.Sub) and self._is_num(node.left) and self._is_num(node.right) and secrets.randbelow(3) == 0:
            neg = ast.UnaryOp(op=ast.USub(), operand=node.right)
            return ast.BinOp(left=node.left, op=ast.Add(), right=neg)
        if isinstance(node.op, ast.Mult) and isinstance(node.right, ast.Constant) and isinstance(node.right.value, int):
            v = node.right.value
            if v > 0 and (v & (v - 1)) == 0 and secrets.randbelow(2) == 0:
                shift = v.bit_length() - 1
                return ast.BinOp(left=node.left, op=ast.LShift(), right=ast.Constant(shift))
        return node


class _BooleanObfuscator(ast.NodeTransformer):
    """Transform True/False into self-equality expressions."""

    def visit_Constant(self, node: ast.Constant):
        if node.value is True and secrets.randbelow(2) == 0:
            x = secrets.randbelow(1000)
            return ast.Compare(
                left=ast.Constant(x), ops=[ast.Eq()], comparators=[ast.Constant(x)])
        if node.value is False and secrets.randbelow(2) == 0:
            x = secrets.randbelow(1000)
            return ast.Compare(
                left=ast.Constant(x), ops=[ast.NotEq()], comparators=[ast.Constant(x)])
        return node


class _LiteralEncryptor(ast.NodeTransformer):
    def __init__(self, cfg: ObfuscateConfig, fdepth=0): self.cfg = cfg; self._fdepth = fdepth
    def visit_FormattedValue(self, n): self._fdepth += 1; r = self.generic_visit(n); self._fdepth -= 1; return r
    def visit_JoinedStr(self, n): self._fdepth += 1; r = self.generic_visit(n); self._fdepth -= 1; return r

    def _xor_encrypt(self, s: str) -> ast.AST:
        """Encrypt string with random XOR key: (lambda k,d: ''.join(chr(b^k)for b in d))(KEY, b'...')"""
        data = s.encode()
        key = secrets.randbelow(256)
        enc = bytes(b ^ key for b in data)
        k_arg = ast.arg(arg="_k", annotation=None)
        d_arg = ast.arg(arg="_d", annotation=None)
        body = ast.Call(
            func=ast.Attribute(value=ast.Constant(""), attr="join"),
            args=[ast.GeneratorExp(
                elt=ast.Call(
                    func=ast.Name(id="chr"),
                    args=[ast.BinOp(
                        left=ast.BinOp(left=ast.Name(id="b"), op=ast.BitXor(), right=ast.Name(id="_k")),
                        op=ast.Add(), right=ast.Constant(0))],
                    keywords=[]),
                generators=[ast.comprehension(
                    target=ast.Name(id="b"),
                    iter=ast.Name(id="_d"),
                    ifs=[], is_async=0)])],
            keywords=[])
        return ast.Call(
            func=ast.Lambda(
                args=ast.arguments(
                    args=[k_arg, d_arg], posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
                body=body),
            args=[ast.Constant(key), ast.Constant(enc)],
            keywords=[])

    def _base64_encrypt(self, s: str) -> ast.Call:
        e = base64.b64encode(s.encode()).decode()
        return ast.Call(func=ast.Attribute(value=ast.Call(func=ast.Attribute(
            value=ast.Call(func=ast.Name(id="__import__"), args=[ast.Constant("base64")], keywords=[]),
            attr="b64decode"), args=[ast.Constant(e)], keywords=[]), attr="decode"), args=[], keywords=[])

    def visit_Constant(self, node):
        if isinstance(node.value, str) and self.cfg.encrypt_strings and len(node.value) > 1 and self._fdepth == 0:
            if self.cfg.string_split and secrets.randbelow(2) == 0:
                return _fragment_string_ast(node.value, secrets.randbelow(3) + 2)
            cipher = self.cfg.string_cipher
            if cipher == "xor" or (cipher == "mixed" and secrets.randbelow(2) == 0):
                return self._xor_encrypt(node.value)
            return self._base64_encrypt(node.value)
        if isinstance(node.value, (int,float)) and not isinstance(node.value, bool) and self.cfg.encrypt_numbers:
            fmt = "i" if isinstance(node.value, int) and -2**31 <= node.value < 2**31 else "q" if isinstance(node.value, int) else "d"
            e = base64.b64encode(struct.pack(fmt, node.value)).decode()
            return ast.Subscript(value=ast.Call(func=ast.Attribute(
                value=ast.Call(func=ast.Name(id="__import__"), args=[ast.Constant("struct")], keywords=[]),
                attr="unpack"), args=[ast.Constant(fmt), ast.Call(func=ast.Attribute(
                value=ast.Call(func=ast.Name(id="__import__"), args=[ast.Constant("base64")], keywords=[]),
                attr="b64decode"), args=[ast.Constant(e)], keywords=[])], keywords=[]), slice=ast.Constant(0), ctx=ast.Load())
        return node


class _StringDisperser(ast.NodeTransformer):
    """Split string constants into fragments scattered across the function.
    At runtime, fragments are joined via ''.join([...]).
    LLMs see fragments in isolation and cannot reconstruct the full string."""

    def __init__(self):
        self._frag_map: dict[str, list[str]] = {}

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, str) and len(node.value) >= 12 and secrets.randbelow(2):
            n = secrets.randbelow(3) + 2
            size = len(node.value) // n
            parts = [node.value[i*size:(i+1)*size] for i in range(n)]
            if len(node.value) % n:
                parts[-1] += node.value[n*size:]
            self._frag_map[node.value] = parts
            return ast.Call(
                func=ast.Attribute(value=ast.Constant(""), attr="join"),
                args=[ast.List(elts=[ast.Constant(p) for p in parts], ctx=ast.Load())],
                keywords=[])
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._frag_map.clear()
        self.generic_visit(node)
        if self._frag_map:
            _scatter_assignments = []
            for _orig, _parts in self._frag_map.items():
                for j, p in enumerate(_parts):
                    _scatter_assignments.append(
                        ast.Assign(targets=[ast.Name(id=f"_f{j}", ctx=ast.Store())],
                                   value=ast.Constant(p), lineno=0))
                    if j > 0:
                        _target_idx = secrets.randbelow(max(1, len(node.body)))
                        node.body.insert(_target_idx, _scatter_assignments[-1])
            if _scatter_assignments:
                node.body.insert(0, _scatter_assignments[0])
        return node


class _OpaqueExprInjector(ast.NodeTransformer):
    """Replace simple ops with complex identities. LLMs can't algebraically simplify."""

    def _is_numeric(self, n: ast.AST) -> bool:
        return isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool)

    def visit_BinOp(self, node: ast.BinOp):
        self.generic_visit(node)
        if not self._is_numeric(node.left) or not self._is_numeric(node.right):
            return node
        if isinstance(node.op, ast.Add) and secrets.randbelow(2):
            return ast.BinOp(left=ast.BinOp(left=node.left, op=ast.BitXor(), right=node.right),
                op=ast.Add(), right=ast.BinOp(left=ast.BinOp(left=node.left, op=ast.BitAnd(), right=node.right),
                op=ast.Mult(), right=ast.Constant(2)))
        if isinstance(node.op, ast.Sub) and secrets.randbelow(2):
            return ast.BinOp(left=ast.BinOp(left=node.left, op=ast.Add(), right=ast.Constant(1)),
                op=ast.Sub(), right=ast.BinOp(left=node.right, op=ast.Add(), right=ast.Constant(1)))
        if isinstance(node.op, ast.Mult) and secrets.randbelow(2):
            return ast.BinOp(left=ast.BinOp(left=ast.BinOp(left=ast.BinOp(left=node.left, op=ast.Add(), right=node.right),
                op=ast.Pow(), right=ast.Constant(2)), op=ast.Sub(), right=ast.BinOp(
                left=ast.BinOp(left=node.left, op=ast.Sub(), right=node.right), op=ast.Pow(),
                right=ast.Constant(2))), op=ast.FloorDiv(), right=ast.Constant(4))
        if isinstance(node.op, ast.BitXor) and secrets.randbelow(2):
            return ast.BinOp(left=ast.BinOp(left=ast.BinOp(left=node.left, op=ast.BitOr(), right=node.right),
                op=ast.Sub(), right=ast.BinOp(left=node.left, op=ast.BitAnd(), right=node.right)),
                op=ast.BitXor(), right=ast.Constant(0))
        return node

    def visit_Compare(self, node: ast.Compare):
        self.generic_visit(node)
        if (len(node.ops) == 1 and isinstance(node.ops[0], ast.Eq)
                and self._is_numeric(node.left) and self._is_numeric(node.comparators[0])
                and secrets.randbelow(2)):
            return ast.Compare(left=ast.BinOp(left=node.left, op=ast.BitXor(), right=node.comparators[0]),
                ops=[ast.Eq()], comparators=[ast.Constant(0)])
        return node
