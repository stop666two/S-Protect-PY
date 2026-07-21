"""Dead code injection obfuscation.

Injects semantically neutral but obfuscating code blocks
that never execute but confuse static analysis.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import ast
import random
import secrets


class DeadCodeInjector(ast.NodeTransformer):
    """Injects dead code blocks into function bodies.

    Dead blocks are guarded by a hash comparison that is always false,
    making them unreachable at runtime while confusing static analysis.
    """

    def __init__(self, density: float = 0.3) -> None:
        """Initialize the injector with a density factor.

        Args:
            density: Probability (0.0 to 1.0) of injecting dead code
                     into any given function.
        """
        self._density = density

    def inject(self, source: str) -> str:
        """Inject dead code into the given source.

        Args:
            source: The Python source code to transform.

        Returns:
            The transformed source code with dead code blocks.
        """
        tree = ast.parse(source)
        tree = self.visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Optionally inject a dead code block into a function.

        Args:
            node: The FunctionDef AST node.

        Returns:
            The potentially modified FunctionDef node.
        """
        node = self.generic_visit(node)
        if random.random() > self._density:
            return node

        guard_value = secrets.token_hex(8)
        guard_hash = secrets.token_hex(32)
        dead_block = ast.If(
            test=ast.Compare(
                left=ast.Call(
                    func=ast.Attribute(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Call(
                                    func=ast.Name(id="__import__", ctx=ast.Load()),
                                    args=[ast.Constant(value="hashlib")],
                                    keywords=[],
                                ),
                                attr="sha256",
                                ctx=ast.Load(),
                            ),
                            args=[ast.Constant(value=guard_value.encode())],
                            keywords=[],
                        ),
                        attr="hexdigest",
                        ctx=ast.Load(),
                    ),
                    args=[],
                    keywords=[],
                ),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=guard_hash)],
            ),
            body=[
                ast.Expr(value=ast.Call(
                    func=ast.Name(id="print", ctx=ast.Load()),
                    args=[ast.Constant(value="")],
                    keywords=[],
                )),
            ],
            orelse=[],
        )
        node.body.insert(0, dead_block)
        return node
