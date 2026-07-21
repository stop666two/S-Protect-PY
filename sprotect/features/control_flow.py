"""Control flow flattening obfuscation.

Transforms structured control flow into a flat dispatch loop with
a state variable, making the code harder to follow statically.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import ast
import secrets


class ControlFlowFlattener(ast.NodeTransformer):
    """Flattens function-level control flow into a state-machine dispatch loop.

    The transformation wraps a function's body statements into a ``while True``
    loop with a state variable and if-dispatch for each original statement.
    Functions with fewer than 3 statements are left unchanged.
    """

    def __init__(self, source: str) -> None:
        """Initialize the flattener with source code.

        Args:
            source: The Python source code to flatten.
        """
        self._source = source

    def flatten(self) -> str:
        """Flatten the control flow of all eligible functions.

        Returns:
            The transformed source code with flattened control flow.
        """
        tree = ast.parse(self._source)
        tree = self.visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Flatten a function definition's body into a state dispatch loop.

        Args:
            node: The FunctionDef AST node.

        Returns:
            The transformed FunctionDef node.
        """
        if not node.body:
            return node
        if len(node.body) < 3:
            return node

        state_var = f"_c_{secrets.token_hex(2)}"

        state_assign = ast.Assign(
            targets=[ast.Name(id=state_var, ctx=ast.Store())],
            value=ast.Constant(value=0),
        )

        dispatcher_body: list[ast.stmt] = []
        last_idx = len(node.body) - 1
        for i, stmt in enumerate(node.body):
            if isinstance(stmt, ast.Return):
                body = [stmt]
            else:
                body = [stmt]
                if i == last_idx:
                    body.append(ast.Break())
                else:
                    body.append(
                        ast.Assign(
                            targets=[ast.Name(id=state_var, ctx=ast.Store())],
                            value=ast.Constant(value=i + 1),
                        )
                    )
                    body.append(ast.Continue())
            if_stmt = ast.If(
                test=ast.Compare(
                    left=ast.Name(id=state_var, ctx=ast.Load()),
                    ops=[ast.Eq()],
                    comparators=[ast.Constant(value=i)],
                ),
                body=body,
                orelse=[],
            )
            dispatcher_body.append(if_stmt)

        dispatcher = ast.While(
            test=ast.Constant(value=True),
            body=dispatcher_body,
            orelse=[],
        )

        node.body = [state_assign, dispatcher]
        return node
