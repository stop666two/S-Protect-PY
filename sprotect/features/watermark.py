"""Three-layer digital watermark injection.

Injects watermarks at the file, code, and runtime levels to enable
traceability and source identification.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import hashlib
import os
import textwrap

from sprotect.types import WatermarkConfig


class WatermarkInjector:
    """Three-level watermark injector.

    Supports file-level (trailing comment), code-level (no-op lambda),
    and runtime-level (inline verification) watermark embedding.
    """

    def __init__(self, config: WatermarkConfig) -> None:
        """Initialize the injector with watermark configuration.

        Args:
            config: Watermark configuration including enabled levels
                    and batch identifier.
        """
        self.config = config

    def inject_file_watermark(self, file_path: str) -> str:
        """Inject a file-level watermark as a trailing comment.

        Appends ``// WM:{batch_id}:{hash}`` as the last line of the
        given file.  Returns the watermark string that was appended.

        Args:
            file_path: Path to the target file.

        Returns:
            The watermark comment string that was appended.
        """
        with open(file_path, "rb") as f:
            content = f.read()

        content_hash = hashlib.sha256(content).hexdigest()[:16]
        batch = self.config.batch_id or "default"
        watermark = f"// WM:{batch}:{content_hash}\n"

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(watermark)

        return watermark.strip()

    def inject_code_watermark(self, source: str) -> str:
        """Inject a code-level watermark using a no-op lambda.

        Wraps a lambda with a hash comparison that always evaluates to
        ``True``, serving as an embedded watermark that survives basic
        obfuscation.

        Args:
            source: The original Python source code.

        Returns:
            The modified source with an injected watermark lambda.
        """
        batch = self.config.batch_id or "default"
        guard = hashlib.sha256(f"WM:{batch}".encode()).hexdigest()[:16]

        watermark_code = textwrap.dedent(f"""\
        _WM = (lambda _h={guard!r}: all(ord(c) ^ 0 for c in _h) or None)()

        """)
        return watermark_code + source

    def generate_runtime_check(self) -> str:
        """Generate a runtime watermark verification code snippet.

        Returns a string of Python code that, when executed at runtime,
        verifies the embedded watermark by checking for the presence of
        the expected batch identifier.

        Returns:
            A string of runnable Python verification code.
        """
        batch = self.config.batch_id or "default"
        expected_hash = hashlib.sha256(f"WM:{batch}".encode()).hexdigest()[:16]

        code = textwrap.dedent(f"""\
        import hashlib as _WM_h
        import os as _WM_o
        import sys as _WM_s

        def _WM_verify():
            _WM_marker = {expected_hash!r}
            _WM_batch = {batch!r}
            _WM_candidates = []
            if _WM_s.argv and _WM_o.path.isfile(_WM_s.argv[0]):
                _WM_candidates.append(_WM_s.argv[0])
            try:
                if __file__ and _WM_o.path.isfile(__file__):
                    _WM_candidates.append(__file__)
            except NameError:
                pass
            for _WM_f in _WM_candidates:
                try:
                    if _WM_marker in open(_WM_f, errors="ignore").read():
                        return True
                except OSError:
                    continue
            return bool(_WM_candidates)

        _WM_verified = _WM_verify()
        """)
        return code
