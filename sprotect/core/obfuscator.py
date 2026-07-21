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


def _collect_definitions(source: str, config: ObfuscateConfig, mapping: dict[str, str]) -> None:
    """Scan source code and collect all function/class definitions into mapping.

    First-pass helper for project builds: builds the rename map without
    transforming code, ensuring cross-module consistency.

    Args:
        source: Python source code.
        config: Obfuscation configuration.
        mapping: Shared rename dict to populate.
    """
    reserved = set(config.rename_rules.reserved or [])
    gen = RandomNameGenerator(
        style=config.rename_rules.style,
        custom_dict=config.rename_rules.dictionary,
    )
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name not in reserved and not node.name.startswith("__"):
                mapping.setdefault(node.name, gen.generate())
        elif isinstance(node, ast.ClassDef):
            if node.name not in reserved and not node.name.startswith("__"):
                mapping.setdefault(node.name, gen.generate())


class Obfuscator(ast.NodeTransformer):
    """AST-based code obfuscation engine.

    Traverses and transforms Python AST nodes to rename identifiers
    (functions, classes, arguments), and to encrypt string and
    numeric literals via base64 and struct expressions.
    """

    def __init__(self, config: ObfuscateConfig, shared_mapping: dict[str, str] | None = None) -> None:
        """Initialize the obfuscator with configuration.

        Args:
            config: Obfuscation configuration including rename rules
                    and encryption settings.
            shared_mapping: Optional shared rename map for cross-file consistency.
                            When building a multi-file project, pass the same dict
                            to all Obfuscator instances so renames stay in sync.
        """
        self.config = config
        self.name_mapping: dict[str, str] = shared_mapping if shared_mapping is not None else {}
        self.reserved = config.rename_rules.reserved
        self.name_gen = RandomNameGenerator(
            style=config.rename_rules.style,
            custom_dict=config.rename_rules.dictionary,
        )
        self._class_depth = 0
        self._fstring_depth = 0
        self._param_stack: list[set[str]] = []

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
        tree = self.visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def visit_alias(self, node: ast.alias) -> ast.alias:
        """Rename imported names (e.g. ``from mod import func``).

        Ensures cross-module imports remain consistent after renaming.

        Args:
            node: The alias AST node.

        Returns:
            The (potentially renamed) alias node.
        """
        if node.name in self.name_mapping:
            node.name = self.name_mapping[node.name]
        return node

    def _push_params(self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda) -> None:
        params: set[str] = set()
        for arg in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
            params.add(arg.arg)
        if node.args.vararg:
            params.add(node.args.vararg.arg)
        if node.args.kwarg:
            params.add(node.args.kwarg.arg)
        self._param_stack.append(params)

    def _pop_params(self) -> None:
        if self._param_stack:
            self._param_stack.pop()

    def _is_param(self, name: str) -> bool:
        return any(name in s for s in self._param_stack)

    def visit_Lambda(self, node: ast.Lambda) -> ast.Lambda:
        self._push_params(node)
        node = self.generic_visit(node)
        self._pop_params()
        return node

    def visit_Name(self, node: ast.Name) -> ast.Name:
        """Rename identifier references that have been obfuscated.

        Skips parameter names of the enclosing function to preserve
        correct parameter binding (e.g. ``lambda a: a + 1``).

        Args:
            node: The Name AST node.

        Returns:
            The (potentially renamed) Name node.
        """
        if node.id in self.name_mapping and not self._is_param(node.id):
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
        self._push_params(node)
        self.generic_visit(node)
        self._pop_params()
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
        self._push_params(node)
        self.generic_visit(node)
        self._pop_params()
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
        """Skip parameter renaming to preserve keyword argument compatibility.
        """
        return node

    def visit_FormattedValue(self, node: ast.FormattedValue) -> ast.FormattedValue:
        self._fstring_depth += 1
        self.generic_visit(node)
        self._fstring_depth -= 1
        return node

    def visit_JoinedStr(self, node: ast.JoinedStr) -> ast.JoinedStr:
        self._fstring_depth += 1
        self.generic_visit(node)
        self._fstring_depth -= 1
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
        if isinstance(node.value, str) and self.config.encrypt_strings and len(node.value) > 1 and self._fstring_depth == 0:
            encoded = base64.b64encode(node.value.encode()).decode()
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Call(
                                func=ast.Name(id="__import__", ctx=ast.Load()),
                                args=[ast.Constant(value="base64")],
                                keywords=[],
                            ),
                            attr="b64decode",
                            ctx=ast.Load(),
                        ),
                        args=[ast.Constant(value=encoded)],
                        keywords=[],
                    ),
                    attr="decode",
                    ctx=ast.Load(),
                ),
                args=[],
                keywords=[],
            )
        if (
            isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
            and self.config.encrypt_numbers
        ):
            if isinstance(node.value, int):
                fmt = "i" if -2**31 <= node.value < 2**31 else "q"
            else:
                fmt = "d"
            packed = struct.pack(fmt, node.value)
            encoded = base64.b64encode(packed).decode()
            return ast.Subscript(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id="__import__", ctx=ast.Load()),
                            args=[ast.Constant(value="struct")],
                            keywords=[],
                        ),
                        attr="unpack",
                        ctx=ast.Load(),
                    ),
                    args=[
                        ast.Constant(value=fmt),
                        ast.Call(
                            func=ast.Attribute(
                                value=ast.Call(
                                    func=ast.Name(id="__import__", ctx=ast.Load()),
                                    args=[ast.Constant(value="base64")],
                                    keywords=[],
                                ),
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
