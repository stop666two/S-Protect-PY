"""AST-based code obfuscation engine.

Transforms Python source code by renaming identifiers, encrypting
string literals, and encrypting numeric literals using the AST.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import ast
import base64
import struct

from sprotect.types import ObfuscateConfig
from sprotect.utils.random_gen import RandomNameGenerator


class Obfuscator(ast.NodeTransformer):
    """AST-based code obfuscation engine.

    Traverses and transforms Python AST nodes to rename identifiers
    (functions, classes, arguments), and to encrypt string and
    numeric literals via base64 and struct expressions.
    """

    def __init__(self, config: ObfuscateConfig) -> None:
        """Initialize the obfuscator with configuration.

        Args:
            config: Obfuscation configuration including rename rules
                    and encryption settings.
        """
        self.config = config
        self.name_mapping: dict[str, str] = {}
        self.reserved = config.rename_rules.reserved
        self.name_gen = RandomNameGenerator(
            style=config.rename_rules.style,
            custom_dict=config.rename_rules.dictionary,
        )
        self._class_depth = 0

    def _get_new_name(self, old_name: str) -> str:
        """Get or create an obfuscated replacement for an identifier.

        Args:
            old_name: The original identifier name.

        Returns:
            The obfuscated replacement name, or the original name
            if it is reserved.
        """
        if old_name.startswith("__") or old_name in self.reserved:
            return old_name
        if old_name not in self.name_mapping:
            self.name_mapping[old_name] = self.name_gen.generate()
        return self.name_mapping[old_name]

    def obfuscate(self, source_code: str) -> str:
        """Obfuscate the given Python source code.

        Parses, transforms, and unparses the source code with
        identifier renaming and literal encryption applied.

        Args:
            source_code: The original Python source code.

        Returns:
            The obfuscated Python source code.
        """
        tree = ast.parse(source_code)
        self._inject_imports(tree)
        tree = self.visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def _inject_imports(self, tree: ast.Module) -> None:
        """Inject required import statements for encryption helpers.

        Inserts 'import base64' and 'import struct' at the top of the
        module when string or number encryption is enabled.

        Args:
            tree: The AST module to modify.
        """
        if self.config.encrypt_numbers:
            tree.body.insert(0, ast.Import(names=[ast.alias(name="struct", asname=None)]))
        if self.config.encrypt_strings or self.config.encrypt_numbers:
            tree.body.insert(0, ast.Import(names=[ast.alias(name="base64", asname=None)]))

    def visit_Name(self, node: ast.Name) -> ast.Name:
        """Rename identifier references that have been obfuscated.

        Args:
            node: The Name AST node.

        Returns:
            The (potentially renamed) Name node.
        """
        if node.id in self.name_mapping:
            node.id = self.name_mapping[node.id]
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Rename standalone function definitions.

        Functions defined directly inside a class body (methods) are
        skipped to preserve attribute-based dispatch.

        Args:
            node: The FunctionDef AST node.

        Returns:
            The transformed FunctionDef node.
        """
        if self.config.rename_functions and self._class_depth == 0:
            node.name = self._get_new_name(node.name)
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        """Rename standalone async function definitions.

        Args:
            node: The AsyncFunctionDef AST node.

        Returns:
            The transformed AsyncFunctionDef node.
        """
        if self.config.rename_functions and self._class_depth == 0:
            node.name = self._get_new_name(node.name)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Rename class definitions.

        Tracks class body depth to prevent renaming methods.

        Args:
            node: The ClassDef AST node.

        Returns:
            The transformed ClassDef node.
        """
        if self.config.rename_classes:
            node.name = self._get_new_name(node.name)
        self._class_depth += 1
        self.generic_visit(node)
        self._class_depth -= 1
        return node

    def visit_arg(self, node: ast.arg) -> ast.arg:
        """Rename function and method arguments.

        Args:
            node: The arg AST node.

        Returns:
            The transformed arg node.
        """
        if self.config.rename_variables:
            node.arg = self._get_new_name(node.arg)
        self.generic_visit(node)
        return node

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        """Encrypt string and numeric literals.

        Replaces string literals (length > 1) with
        ``base64.b64decode("...")`` expressions, and numeric
        literals with ``struct.unpack("d", base64.b64decode("..."))[0]``
        expressions.

        Args:
            node: The Constant AST node.

        Returns:
            The original Constant or an encrypted expression node.
        """
        if isinstance(node.value, str) and self.config.encrypt_strings and len(node.value) > 1:
            encoded = base64.b64encode(node.value.encode()).decode()
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="base64", ctx=ast.Load()),
                    attr="b64decode",
                    ctx=ast.Load(),
                ),
                args=[ast.Constant(value=encoded)],
                keywords=[],
            )
        if (
            isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
            and self.config.encrypt_numbers
        ):
            packed = struct.pack("d", node.value)
            encoded = base64.b64encode(packed).decode()
            return ast.Subscript(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="struct", ctx=ast.Load()),
                        attr="unpack",
                        ctx=ast.Load(),
                    ),
                    args=[
                        ast.Constant(value="d"),
                        ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="base64", ctx=ast.Load()),
                                attr="b64decode",
                                ctx=ast.Load(),
                            ),
                            args=[ast.Constant(value=encoded)],
                            keywords=[],
                        ),
                    ],
                    keywords=[],
                ),
                slice=ast.Constant(value=0),
                ctx=ast.Load(),
            )
        return node
