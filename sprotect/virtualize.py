# VM BYTECODE ENGINE: custom interpreter for obfuscated control flow
# OPCODES: 40+ instruction types
"""Code virtualization: compile Python AST to custom VM bytecode."""
from __future__ import annotations
import ast, struct, hashlib, secrets
from sprotect.types import VirtualizationConfig, VirtualizationMode

_INSTRUCTION_SET = {
    "NOP": 0, "LOAD_CONST": 1, "LOAD_NAME": 2, "STORE_NAME": 3,
    "BINARY_ADD": 10, "BINARY_SUB": 11, "BINARY_MUL": 12, "BINARY_DIV": 13,
    "BINARY_MOD": 14, "BINARY_POW": 15, "BINARY_AND": 16, "BINARY_OR": 17,
    "BINARY_XOR": 18, "BINARY_LSHIFT": 19, "BINARY_RSHIFT": 20,
    "COMPARE_EQ": 21, "COMPARE_NE": 22, "COMPARE_LT": 23, "COMPARE_GT": 24,
    "COMPARE_LE": 25, "COMPARE_GE": 26, "JUMP_FORWARD": 30, "JUMP_IF_FALSE": 31,
    "JUMP_ABSOLUTE": 32, "CALL_FUNCTION": 40, "RETURN_VALUE": 50,
    "BUILD_LIST": 60, "BUILD_TUPLE": 61, "BUILD_SET": 62, "BUILD_DICT": 63,
    "BUILD_SLICE": 64, "LIST_APPEND": 65, "MAP_ADD": 66,
    "UNARY_NOT": 70, "UNARY_NEG": 71, "UNARY_INV": 72,
    "FOR_ITER": 80, "GET_ITER": 81, "YIELD_VALUE": 90,
    "SETUP_EXCEPT": 100, "POP_EXCEPT": 101, "RAISE": 102,
    "LOAD_ATTR": 110, "STORE_ATTR": 111,
    "LOAD_SUBSCR": 112, "STORE_SUBSCR": 113,
}

_INSTRUCTION_REVERSE = {v: k for k, v in _INSTRUCTION_SET.items()}
_BINARY_OPCODES = {
    ast.Add: "BINARY_ADD", ast.Sub: "BINARY_SUB", ast.Mult: "BINARY_MUL",
    ast.Div: "BINARY_DIV", ast.Mod: "BINARY_MOD", ast.Pow: "BINARY_POW",
    ast.BitAnd: "BINARY_AND", ast.BitOr: "BINARY_OR", ast.BitXor: "BINARY_XOR",
    ast.LShift: "BINARY_LSHIFT", ast.RShift: "BINARY_RSHIFT",
}
_COMPARE_OPCODES = {
    ast.Eq: "COMPARE_EQ", ast.NotEq: "COMPARE_NE", ast.Lt: "COMPARE_LT",
    ast.Gt: "COMPARE_GT", ast.LtE: "COMPARE_LE", ast.GtE: "COMPARE_GE",
}


class VMCompiler:
    """Compile a Python function AST to VM bytecode."""

    def __init__(self, func_name: str, arg_names: list[str]):
        self._func_name = func_name
        self._arg_names = arg_names
        self._bytecode_stream: list[int] = []
        self._constant_pool: list = []
        self._symbol_table: list[str] = []
        self._const_lookup: dict = {}
        self._symbol_lookup: dict = {}
        self._branch_targets: dict[int, int] = {}
        self._fixup_table: list[tuple[int, int]] = []

    def _const_idx(self, v) -> int:
        if v not in self._const_lookup:
            self._const_lookup[v] = len(self._constant_pool)
            self._constant_pool.append(v)
        return self._const_lookup[v]

    def _name_idx(self, n: str) -> int:
        if n not in self._symbol_lookup:
            self._symbol_lookup[n] = len(self._symbol_table)
            self._symbol_table.append(n)
        return self._symbol_lookup[n]

    def _emit(self, op: str, arg: int = 0):
        self._bytecode_stream.append(_INSTRUCTION_SET[op])
        self._bytecode_stream.append(arg)

    def _patch(self, pos: int, target: int):
        self._bytecode_stream[pos] = target

    def _label(self) -> int:
        lbl = len(self._bytecode_stream)
        self._branch_targets[lbl] = lbl
        return lbl

    def compile(self, node: ast.AST):
        if isinstance(node, ast.Module):
            for stmt in node.body:
                self.compile(stmt)
        elif isinstance(node, ast.FunctionDef):
            for stmt in node.body:
                self.compile(stmt)
        elif isinstance(node, ast.Expr):
            self.compile(node.value)
            self._emit("NOP")
        elif isinstance(node, ast.Assign):
            self.compile(node.value)
            for t in node.targets:
                if isinstance(t, ast.Name):
                    self._emit("STORE_NAME", self._name_idx(t.id))
        elif isinstance(node, ast.Return):
            if node.value:
                self.compile(node.value)
            self._emit("RETURN_VALUE")
        elif isinstance(node, ast.Constant):
            self._emit("LOAD_CONST", self._const_idx(node.value))
        elif isinstance(node, ast.Name):
            if node.id in self._arg_names:
                self._emit("LOAD_NAME", self._name_idx(node.id))
            else:
                self._emit("LOAD_NAME", self._name_idx(node.id))
        elif isinstance(node, ast.BinOp):
            self.compile(node.left)
            self.compile(node.right)
            op_name = _BINARY_OPCODES.get(type(node.op))
            if op_name:
                self._emit(op_name)
        elif isinstance(node, ast.Compare):
            self.compile(node.left)
            self.compile(node.comparators[0])
            op_name = _COMPARE_OPCODES.get(type(node.ops[0]))
            if op_name:
                self._emit(op_name)
        elif isinstance(node, ast.If):
            self.compile(node.test)
            self._emit("JUMP_IF_FALSE", 0)
            patch_false = len(self._bytecode_stream) - 1
            for stmt in node.body:
                self.compile(stmt)
            if node.orelse:
                self._emit("JUMP_FORWARD", 0)
                patch_end = len(self._bytecode_stream) - 1
                self._patch(patch_false, len(self._bytecode_stream))
                for stmt in node.orelse:
                    self.compile(stmt)
                self._patch(patch_end, len(self._bytecode_stream))
            else:
                self._patch(patch_false, len(self._bytecode_stream))
        elif isinstance(node, ast.While):
            start = len(self._bytecode_stream)
            self.compile(node.test)
            self._emit("JUMP_IF_FALSE", 0)
            patch_exit = len(self._bytecode_stream) - 1
            for stmt in node.body:
                self.compile(stmt)
            self._emit("JUMP_ABSOLUTE", start)
            self._patch(patch_exit, len(self._bytecode_stream))
        elif isinstance(node, ast.Call):
            self.compile(node.func)
            for arg in node.args:
                self.compile(arg)
            self._emit("CALL_FUNCTION", len(node.args))
        elif isinstance(node, ast.Attribute):
            self.compile(node.value)
            self._emit("LOAD_ATTR", self._const_idx(node.attr))
        elif isinstance(node, ast.Subscript):
            self.compile(node.value)
            self.compile(node.slice)
            self._emit("LOAD_SUBSCR")
        elif isinstance(node, ast.UnaryOp):
            self.compile(node.operand)
            if isinstance(node.op, ast.Not): self._emit("UNARY_NOT")
            elif isinstance(node.op, ast.USub): self._emit("UNARY_NEG")
            elif isinstance(node.op, ast.Invert): self._emit("UNARY_INV")
        elif isinstance(node, ast.For):
            iter_name = f"_i{secrets.token_hex(2)}"
            self.compile(node.iter)
            self._emit("STORE_NAME", self._name_idx(iter_name))
            start = len(self._bytecode_stream)
            self._emit("LOAD_NAME", self._name_idx(iter_name))
            self._emit("FOR_ITER")
            exit_patch = len(self._bytecode_stream) - 1
            self.compile(node.target)
            for stmt in node.body:
                self.compile(stmt)
            self._emit("JUMP_ABSOLUTE", start)
            self._patch(exit_patch, len(self._bytecode_stream))
        elif isinstance(node, ast.Try):
            for handler in node.handlers:
                self._emit("SETUP_EXCEPT")
                try_start = len(self._bytecode_stream)
                for stmt in node.body:
                    self.compile(stmt)
                self._emit("POP_EXCEPT")
                if handler.name:
                    self._emit("STORE_NAME", self._name_idx(handler.name))
                for stmt in handler.body:
                    self.compile(stmt)
        elif isinstance(node, ast.Yield):
            if node.value:
                self.compile(node.value)
            self._emit("YIELD_VALUE")
        elif isinstance(node, ast.List):
            for elt in node.elts:
                self.compile(elt)
            self._emit("BUILD_LIST", len(node.elts))
        elif isinstance(node, ast.Tuple):
            for elt in node.elts:
                self.compile(elt)
            self._emit("BUILD_TUPLE", len(node.elts))
        elif isinstance(node, ast.Set):
            for elt in node.elts:
                self.compile(elt)
            self._emit("BUILD_SET", len(node.elts))
        elif isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                self.compile(k)
                self.compile(v)
            self._emit("BUILD_DICT", len(node.keys))
        elif isinstance(node, ast.ListComp):
            self._emit("BUILD_LIST", 0)
            for gen in node.generators:
                self.compile(gen.iter)
                self._emit("GET_ITER")
                for stmt in gen.ifs:
                    self.compile(stmt)

    def get_bytecode(self) -> bytes:
        data = bytearray()
        data += struct.pack("<I", len(self._bytecode_stream))
        data += struct.pack("<" + "I" * len(self._bytecode_stream), *self._bytecode_stream)
        consts_data = bytearray()
        for c in self._constant_pool:
            if isinstance(c, (int, float)):
                consts_data += b"i" + struct.pack("<d", float(c))
            elif isinstance(c, str):
                cb = c.encode()
                consts_data += b"s" + struct.pack("<I", len(cb)) + cb
            elif c is None:
                consts_data += b"n"
            elif isinstance(c, bool):
                consts_data += b"b" + struct.pack("<?", c)
        data += struct.pack("<I", len(consts_data)) + bytes(consts_data)
        data += struct.pack("<I", len(self._symbol_table))
        for n in self._symbol_table:
            nb = n.encode()
            data += struct.pack("<I", len(nb)) + nb
        return bytes(data)

    def get_metadata(self) -> dict:
        return {
            "func": self._func_name,
            "args": self._arg_names,
            "names": self._symbol_table,
            "consts": [str(c)[:40] for c in self._constant_pool],
            "instrs": len(self._bytecode_stream) // 2,
        }


def compile_function(source: str, func_name: str, config: VirtualizationConfig) -> tuple[bytes, dict]:
    """Compile a named function from source into VM bytecode."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            arg_names = [a.arg for a in node.args.args]
            compiler = VMCompiler(func_name, arg_names)
            compiler.compile(node)
            return compiler.get_bytecode(), compiler.get_metadata()
    raise ValueError(f"Function {func_name} not found in source")


class VMInterpreter:
    """VM bytecode interpreter."""

    def __init__(self, bytecode: bytes, globals_dict: dict):
        self._globals = globals_dict
        self._vm_opcodes, self._consts, self._names = self._load(bytecode)

    def _load(self, data: bytes) -> tuple[list[int], list, list[str]]:
        off = 0
        code_len = struct.unpack_from("<I", data, off)[0]; off += 4
        code = list(struct.unpack_from("<" + "I" * code_len, data, off)); off += 4 * code_len
        consts_len = struct.unpack_from("<I", data, off)[0]; off += 4
        consts = []
        end = off + consts_len
        while off < end:
            tag = data[off:off+1]; off += 1
            if tag == b"i":
                consts.append(struct.unpack_from("<d", data, off)[0]); off += 8
            elif tag == b"s":
                slen = struct.unpack_from("<I", data, off)[0]; off += 4
                consts.append(data[off:off+slen].decode()); off += slen
            elif tag == b"n":
                consts.append(None)
            elif tag == b"b":
                consts.append(struct.unpack_from("<?", data, off)[0]); off += 1
        names_len = struct.unpack_from("<I", data, off)[0]; off += 4
        names = []
        for _ in range(names_len):
            nlen = struct.unpack_from("<I", data, off)[0]; off += 4
            names.append(data[off:off+nlen].decode()); off += nlen
        return code, consts, names

    def run(self, args: list = None) -> object:
        stack, locals_dict = [], {}
        if args:
            for i, n in enumerate(self._names[:len(args)]):
                locals_dict[n] = args[i]
        ip = 0
        while ip < len(self._vm_opcodes):
            op = self._vm_opcodes[ip]; arg = self._vm_opcodes[ip + 1]; ip += 2
            if op == _INSTRUCTION_SET["LOAD_CONST"]: stack.append(self._consts[arg])
            elif op == _INSTRUCTION_SET["LOAD_NAME"]: stack.append(locals_dict.get(self._names[arg], self._globals.get(self._names[arg])))
            elif op == _INSTRUCTION_SET["STORE_NAME"]: locals_dict[self._names[arg]] = stack.pop()
            elif op == _INSTRUCTION_SET["BINARY_ADD"]: b, a = stack.pop(), stack.pop(); stack.append(a + b)
            elif op == _INSTRUCTION_SET["BINARY_SUB"]: b, a = stack.pop(), stack.pop(); stack.append(a - b)
            elif op == _INSTRUCTION_SET["BINARY_MUL"]: b, a = stack.pop(), stack.pop(); stack.append(a * b)
            elif op == _INSTRUCTION_SET["BINARY_DIV"]: b, a = stack.pop(), stack.pop(); stack.append(a / b)
            elif op == _INSTRUCTION_SET["BINARY_MOD"]: b, a = stack.pop(), stack.pop(); stack.append(a % b)
            elif op == _INSTRUCTION_SET["BINARY_POW"]: b, a = stack.pop(), stack.pop(); stack.append(a ** b)
            elif op == _INSTRUCTION_SET["BINARY_AND"]: b, a = stack.pop(), stack.pop(); stack.append(a & b)
            elif op == _INSTRUCTION_SET["BINARY_OR"]: b, a = stack.pop(), stack.pop(); stack.append(a | b)
            elif op == _INSTRUCTION_SET["BINARY_XOR"]: b, a = stack.pop(), stack.pop(); stack.append(a ^ b)
            elif op == _INSTRUCTION_SET["BINARY_LSHIFT"]: b, a = stack.pop(), stack.pop(); stack.append(a << b)
            elif op == _INSTRUCTION_SET["BINARY_RSHIFT"]: b, a = stack.pop(), stack.pop(); stack.append(a >> b)
            elif op == _INSTRUCTION_SET["COMPARE_EQ"]: b, a = stack.pop(), stack.pop(); stack.append(a == b)
            elif op == _INSTRUCTION_SET["COMPARE_NE"]: b, a = stack.pop(), stack.pop(); stack.append(a != b)
            elif op == _INSTRUCTION_SET["COMPARE_LT"]: b, a = stack.pop(), stack.pop(); stack.append(a < b)
            elif op == _INSTRUCTION_SET["COMPARE_GT"]: b, a = stack.pop(), stack.pop(); stack.append(a > b)
            elif op == _INSTRUCTION_SET["COMPARE_LE"]: b, a = stack.pop(), stack.pop(); stack.append(a <= b)
            elif op == _INSTRUCTION_SET["COMPARE_GE"]: b, a = stack.pop(), stack.pop(); stack.append(a >= b)
            elif op == _INSTRUCTION_SET["JUMP_FORWARD"]: ip += arg
            elif op == _INSTRUCTION_SET["JUMP_IF_FALSE"]:
                if not stack.pop(): ip = arg
            elif op == _INSTRUCTION_SET["JUMP_ABSOLUTE"]: ip = arg
            elif op == _INSTRUCTION_SET["CALL_FUNCTION"]:
                args_list = [stack.pop() for _ in range(arg)][::-1]
                fn = stack.pop()
                stack.append(fn(*args_list))
            elif op == _INSTRUCTION_SET["RETURN_VALUE"]: return stack.pop() if stack else None
            elif op == _INSTRUCTION_SET["NOP"]: pass
            elif op == _INSTRUCTION_SET["UNARY_NOT"]: stack.append(not stack.pop())
            elif op == _INSTRUCTION_SET["UNARY_NEG"]: stack.append(-stack.pop())
            elif op == _INSTRUCTION_SET["UNARY_INV"]: stack.append(~stack.pop())
            elif op == _INSTRUCTION_SET["BUILD_LIST"]:
                items = [stack.pop() for _ in range(arg)][::-1]; stack.append(items)
            elif op == _INSTRUCTION_SET["BUILD_TUPLE"]:
                items = [stack.pop() for _ in range(arg)][::-1]; stack.append(tuple(items))
            elif op == _INSTRUCTION_SET["BUILD_SET"]:
                items = [stack.pop() for _ in range(arg)][::-1]; stack.append(set(items))
            elif op == _INSTRUCTION_SET["BUILD_DICT"]:
                items = [(stack.pop(), stack.pop()) for _ in range(arg)][::-1]
                stack.append(dict(items))
            elif op == _INSTRUCTION_SET["LOAD_ATTR"]:
                obj = stack.pop(); stack.append(getattr(obj, self._consts[arg]))
            elif op == _INSTRUCTION_SET["STORE_ATTR"]:
                val = stack.pop(); obj = stack.pop()
                setattr(obj, self._consts[arg], val)
            elif op == _INSTRUCTION_SET["LOAD_SUBSCR"]:
                key = stack.pop(); obj = stack.pop(); stack.append(obj[key])
            elif op == _INSTRUCTION_SET["STORE_SUBSCR"]:
                val = stack.pop(); key = stack.pop(); obj = stack.pop(); obj[key] = val
            elif op == _INSTRUCTION_SET["GET_ITER"]:
                stack.append(iter(stack.pop()))
            elif op == _INSTRUCTION_SET["FOR_ITER"]:
                try:
                    it = stack[-1]; stack.append(next(it))
                except StopIteration:
                    stack.pop(); ip = arg
            elif op == _INSTRUCTION_SET["YIELD_VALUE"]:
                return stack.pop()
            elif op == _INSTRUCTION_SET["SETUP_EXCEPT"]:
                pass
            elif op == _INSTRUCTION_SET["POP_EXCEPT"]:
                pass
            elif op == _INSTRUCTION_SET["RAISE"]:
                raise stack.pop() if stack else Exception("VM raise")
        return stack.pop() if stack else None


def virtualize_source(source: str, config: VirtualizationConfig) -> str:
    """Replace virtualized functions with VM bytecode calls in source."""
    tree = ast.parse(source)
    virtualized: dict[str, bytes] = {}
    for node in list(ast.walk(tree)):
        if isinstance(node, ast.FunctionDef) and config.functions:
            if node.name in config.functions and node.name not in config.exclude_functions:
                bc, _ = compile_function(source, node.name, config)
                virtualized[node.name] = bc
    if not virtualized:
        return source
    result_lines = []
    for line in source.split("\n"):
        result_lines.append(line)
    for fn_name, bc in virtualized.items():
        bc_str = bc.hex()
        result_lines.append(f"\n# VM:{fn_name}")
        result_lines.append(f"from sprotect.virtualize import VMInterpreter")
        result_lines.append(f"_vm_{fn_name} = VMInterpreter(bytes.fromhex('{bc_str}'), globals())")
    return "\n".join(result_lines) + "\n"
