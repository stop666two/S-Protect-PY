"""Random name generator for identifier obfuscation.

Provides various naming styles including HEX, Chinese characters,
invisible Unicode, mathematical symbols, and custom dictionary lookups.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import random
import secrets

from sprotect.types import NamingStyle


class RandomNameGenerator:
    """Generate obfuscated identifiers in various naming styles.

    Supports HEX, CHINESE, INVISIBLE, MATH_SYMBOLS, and CUSTOM styles
    for use in code obfuscation rename operations.
    """

    _CHINESE_CHARS = (
        "的一是不了人我在有他这为之大来以个中上们到说时"
        "要就你会子可道得自么然家国过着想去看能天那多小"
        "下生心动而发成于事如法开发东西加主出力学分什么"
    )
    _MATH_SYMBOLS = "αβγδεζηθικλμνξοπρστυφχψω"

    def __init__(
        self,
        style: NamingStyle,
        custom_dict: dict[str, str] | None = None,
    ) -> None:
        """Initialize the generator with a naming style.

        Args:
            style: The naming style to use for generated identifiers.
            custom_dict: Optional dictionary for CUSTOM style lookups.
        """
        self.style = style
        self.custom_dict = custom_dict or {}
        self._counter = 0

    def generate(self) -> str:
        """Generate a random identifier based on the configured style.

        Returns:
            A randomly generated identifier string.
        """
        if self.style == NamingStyle.HEX:
            return "_0x" + secrets.token_hex(4)
        if self.style == NamingStyle.CHINESE:
            return random.choice(self._CHINESE_CHARS) + random.choice(self._CHINESE_CHARS)
        if self.style == NamingStyle.INVISIBLE:
            self._counter += 1
            return "\u200b\u200c\u200d" + str(self._counter)
        if self.style == NamingStyle.MATH_SYMBOLS:
            return random.choice(self._MATH_SYMBOLS) + random.choice(self._MATH_SYMBOLS)
        if self.style == NamingStyle.CUSTOM:
            if self.custom_dict:
                key = random.choice(list(self.custom_dict.keys()))
                return self.custom_dict[key]
            return self._fallback()
        return self._fallback()

    def _fallback(self) -> str:
        """Fallback to HEX style when CUSTOM has no dictionary."""
        return "_0x" + secrets.token_hex(4)
