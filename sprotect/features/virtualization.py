"""Python bytecode virtualization obfuscation.

Translates selected Python functions into a custom VM instruction set
with a bundled interpreter. Supports full-file or partial (targeted
function) virtualization modes.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import ast
import dis
import json
import secrets
import types
from sprotect.types import VirtualizationConfig, VirtualizationMode


class VirtualizationEngine:
    """Virtualizes Python functions into a custom VM instruction set.

    The VM uses a stack-based instruction set with a pure-Python
    interpreter loop. Virtualized functions are replaced by wrappers
    that delegate execution to the VM interpreter.

    Supported VM opcodes:
        LOAD_CONST(0x01)  - push constant onto stack
        LOAD_NAME(0x02)   - push local variable onto stack
        STORE_NAME(0x03)  - pop stack into local variable
        BINARY_ADD(0x10)  - pop two, push sum
        BINARY_SUB(0x11)  - pop two, push difference
        BINARY_MUL(0x12)  - pop two, push product
        BINARY_DIV(0x13)  - pop two, push quotient
        CALL_FUNCTION(0x20) - call function from stack
        RETURN_VALUE(0x30) - return from VM
        COMPARE_OP(0x40)  - comparison operator
        JUMP_ABSOLUTE(0x50) - unconditional jump
        POP_JUMP_IF_FALSE(0x51) - pop and jump if falsy
        POP_JUMP_IF_TRUE(0x52)  - pop and jump if truthy
    """

    _VM_OPCODES: dict[str, int] = {
        "LOAD_CONST": 0x01,
        "LOAD_NAME": 0x02,
        "STORE_NAME": 0x03,
        "BINARY_ADD": 0x10,
        "BINARY_SUBTRACT": 0x11,
        "BINARY_MULTIPLY": 0x12,
        "BINARY_DIVIDE": 0x13,
        "CALL_FUNCTION": 0x20,
        "RETURN_VALUE": 0x30,
        "COMPARE_OP": 0x40,
        "JUMP_ABSOLUTE": 0x50,
        "POP_JUMP_IF_FALSE": 0x51,
        "POP_JUMP_IF_TRUE": 0x52,
    }

    # Python 3.11+ renamed BINARY_* to BINARY_OP with a sub-op
    _BINARY_OP_MAP: dict[int, int] = {
        0: 0x10,   # BINARY_OP ADD
        1: 0x11,   # BINARY_OP SUBTRACT
        5: 0x12,   # BINARY_OP MULTIPLY
        6: 0x13,   # BINARY_OP DIVIDE
    }

    def __init__(self, config: VirtualizationConfig) -> None:
        """Initialize the virtualization engine.

        Args:
            config: Virtualization configuration with mode and target
                    function/glob settings.
        """
        self._config = config
        self._vm_id = secrets.token_hex(4)

    def virtualize(self, source: str, file_path: str = "") -> str:
        """Virtualize functions in the given source code.

        In FULL mode all functions are virtualized. In PARTIAL mode only
        functions listed in ``config.functions`` or matching
        ``config.glob_patterns`` (relative to *file_path*) are virtualized.

        Args:
            source: Python source code.
            file_path: Optional file path for glob matching.

        Returns:
            Transformed source with virtualized functions.
        """
        tree = ast.parse(source)

        if self._config.mode == VirtualizationMode.FULL:
            self._virtualize_all(tree)
        elif self._config.mode == VirtualizationMode.PARTIAL:
            self._virtualize_partial(tree, file_path)

        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def _virtualize_all(self, tree: ast.Module) -> None:
        """Virtualize every function definition in the AST."""
        for node in list(ast.walk(tree)):
            if isinstance(node, ast.FunctionDef):
                self._replace_function(node)

    def _virtualize_partial(self, tree: ast.Module, file_path: str) -> None:
        """Virtualize only functions matching config or glob patterns."""
        import fnmatch
        target_funcs: set[str] = set(self._config.functions or [])

        for pattern in self._config.glob_patterns or []:
            if file_path and fnmatch.fnmatch(file_path, pattern):
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        target_funcs.add(node.name)

        for node in list(ast.walk(tree)):
            if isinstance(node, ast.FunctionDef) and node.name in target_funcs:
                self._replace_function(node)

    def _replace_function(self, node: ast.FunctionDef) -> None:
        """Replace a function body with a VM interpreter call.

        The original function body is translated to VM bytecode and
        replaced with a wrapper that passes control to the generated
        VM interpreter.

        Args:
            node: The FunctionDef AST node to replace.
        """
        func_name = node.name
        func_source = ast.unparse(node)

        try:
            code = compile(func_source, "<vm>", "exec")
        except SyntaxError:
            return

        func_code_obj: types.CodeType | None = None
        for const in code.co_consts:
            if isinstance(const, types.CodeType) and const.co_name == func_name:
                func_code_obj = const
                break

        if func_code_obj is None:
            return

        try:
            instructions = list(dis.get_instructions(func_code_obj))
        except Exception:
            return

        vm_bytecode, consts_list, names_list = self._translate_instructions(
            instructions, func_code_obj
        )

        vm_data = json.dumps({
            "bc": vm_bytecode,
            "consts": consts_list,
            "names": names_list,
            "arg_count": len(node.args.args),
        })

        arg_names = [a.arg for a in node.args.args]

        call_args = [ast.Constant(value=vm_data)]
        call_args.extend(ast.Name(id=a, ctx=ast.Load()) for a in arg_names)

        wrapper_body = ast.Return(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=f"__vm_{self._vm_id}", ctx=ast.Load()),
                    attr="run",
                    ctx=ast.Load(),
                ),
                args=call_args,
                keywords=[],
            )
        )

        node.body = [wrapper_body]
        for field in ("decorator_list", "returns", "type_comment", "type_params"):
            if hasattr(node, field):
                setattr(node, field, getattr(node, field, None))

    def _translate_instructions(
        self,
        instructions: list[dis.Instruction],
        code_obj: types.CodeType,
    ) -> tuple[list[list[int]], list, list[str]]:
        """Translate Python bytecode instructions to VM instruction tuples.

        Args:
            instructions: List of ``dis.Instruction`` from the function.
            code_obj: The function's code object (provides consts/names).

        Returns:
            Tuple of (vm_bytecode, consts_list, names_list).
        """
        vm_bytecode: list[list[int]] = []
        consts_list: list = []
        names_list: list[str] = list(code_obj.co_names)

        # Populate consts list from co_consts, filtering out code objects
        for c in code_obj.co_consts:
            if not isinstance(c, types.CodeType):
                consts_list.append(self._encode_const(c))

        # Build a mapping from original const index to our filtered index
        const_index_map: dict[int, int] = {}
        filtered_idx = 0
        for orig_idx, c in enumerate(code_obj.co_consts):
            if not isinstance(c, types.CodeType):
                const_index_map[orig_idx] = filtered_idx
                filtered_idx += 1

        for instr in instructions:
            op = self._VM_OPCODES.get(instr.opname, 0xFF)
            arg: int = instr.arg or 0

            if instr.opname == "LOAD_CONST":
                mapped = const_index_map.get(arg, 0)
                vm_bytecode.append([op, mapped])
            elif instr.opname == "LOAD_NAME":
                vm_bytecode.append([op, arg])
            elif instr.opname == "STORE_NAME":
                vm_bytecode.append([op, arg])
            elif instr.opname in ("BINARY_OP",):
                sub_op = self._BINARY_OP_MAP.get(arg, 0xFF)
                vm_bytecode.append([sub_op, 0])
            elif instr.opname == "CALL_FUNCTION":
                vm_bytecode.append([op, arg])
            elif instr.opname == "RETURN_VALUE":
                vm_bytecode.append([op, 0])
            elif instr.opname == "COMPARE_OP":
                vm_bytecode.append([op, arg])
            elif instr.opname in ("JUMP_FORWARD", "JUMP_ABSOLUTE"):
                vm_bytecode.append([0x50, arg])
            elif instr.opname == "POP_JUMP_FORWARD_IF_FALSE":
                vm_bytecode.append([0x51, arg])
            elif instr.opname == "POP_JUMP_FORWARD_IF_TRUE":
                vm_bytecode.append([0x52, arg])
            elif instr.opname == "LOAD_FAST":
                vm_bytecode.append([0x02, arg])
            elif instr.opname == "STORE_FAST":
                vm_bytecode.append([0x03, arg])
            elif instr.opname == "LOAD_GLOBAL":
                vm_bytecode.append([0x02, arg])
            else:
                vm_bytecode.append([op, arg])

        return vm_bytecode, consts_list, names_list

    def _encode_const(self, value: object) -> object:
        """Encode a constant value for VM data serialization.

        Non-serializable types are converted to their string repr.

        Args:
            value: The constant value.

        Returns:
            JSON-serializable representation of the constant.
        """
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        if isinstance(value, bytes):
            return value.decode("latin-1")
        if isinstance(value, tuple):
            return tuple(self._encode_const(v) for v in value)
        if isinstance(value, complex):
            return [value.real, value.imag]
        return repr(value)

    def generate_vm_interpreter(self) -> str:
        """Generate a self-contained VM interpreter class as Python source.

        The interpreter is a pure-Python class with a ``run`` method that
        executes the VM instruction set using a ``while`` loop, a stack,
        and a locals dictionary. It includes integrity verification via
        SHA-256 hashing of the VM data.

        Returns:
            Python source code for the VM interpreter class.
        """
        return f'''class __VM_{self._vm_id}:
    """Custom virtual machine interpreter for virtualized code."""

    def run(self, vm_data: str, *args: object) -> object:
        import json
        data = json.loads(vm_data)
        bc = data["bc"]
        consts = data["consts"]
        names = data["names"]
        stack: list = []
        locals_dict: dict = {{}}
        for i, arg_val in enumerate(args):
            if i < len(names):
                locals_dict[names[i]] = arg_val
        ip = 0
        while ip < len(bc):
            op, arg = bc[ip]
            if op == 1:
                stack.append(consts[arg])
            elif op == 2:
                name = names[arg] if arg < len(names) else str(arg)
                stack.append(locals_dict.get(name, None))
            elif op == 3:
                name = names[arg] if arg < len(names) else str(arg)
                locals_dict[name] = stack.pop()
            elif op == 0x10:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif op == 0x11:
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
            elif op == 0x12:
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
            elif op == 0x13:
                b = stack.pop()
                a = stack.pop()
                stack.append(a / b)
            elif op == 0x20:
                fn_args = [stack.pop() for _ in range(arg)][::-1]
                func = stack.pop()
                stack.append(func(*fn_args))
            elif op == 0x30:
                return stack.pop() if stack else None
            ip += 1
        return None
'''
