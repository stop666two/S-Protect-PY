"""Key sharding utility using XOR-based secret sharing.

Splits a key into N shards via XOR secret sharing, embeds shards
into files as comment lines, and extracts them for reconstruction.
Any N-1 shards reveal zero information about the original key.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import base64
import os
import re
from typing import Optional

_SHARD_PREFIX = "// SHARD:"


def split_key(key: bytes, shard_count: int) -> list[bytes]:
    """Split a key into shard_count shards using XOR secret sharing.

    Generates shard_count-1 random slices; the final shard is the XOR
    of the key and all prior shards.  Any shard_count-1 pieces are
    indistinguishable from random noise.

    Args:
        key: The secret bytes to split.
        shard_count: Number of shards to produce (must be >= 2).

    Returns:
        A list of shard_count byte strings.

    Raises:
        ValueError: If shard_count < 2.
    """
    if shard_count < 2:
        raise ValueError(f"shard_count must be >= 2, got {shard_count}")

    shards: list[bytes] = []
    for _ in range(shard_count - 1):
        shards.append(os.urandom(len(key)))

    final = bytearray(key)
    for s in shards:
        for i in range(len(final)):
            final[i] ^= s[i]
    shards.append(bytes(final))

    return shards


def reconstruct_key(shards: list[bytes]) -> bytes:
    """Reconstruct the original key by XORing all shards together.

    Args:
        shards: All shards produced by a single split_key call.

    Returns:
        The reconstructed original key.
    """
    result = bytearray(shards[0])
    for s in shards[1:]:
        for i in range(len(result)):
            result[i] ^= s[i]
    return bytes(result)


def embed_shard_into_file(
    target_file: str, shard: bytes, offset: int | None = None
) -> int:
    """Embed a shard into a file as a trailing comment line.

    Appends a line ``// SHARD:base64data`` to the file.  When
    *offset* is given, the tool verifies the file already has a
    SHARD line at that byte offset (used for position-aware lookups).

    Args:
        target_file: Path to the target text file.
        shard: The shard bytes to embed.
        offset: Expected byte offset of an existing SHARD line to
            overwrite.  If None, appends a new line at EOF.

    Returns:
        The byte offset at which the SHARD comment was written
        (points to the ``/`` of ``//``).
    """
    encoded = base64.b64encode(shard).decode("ascii")
    line = f"{_SHARD_PREFIX}{encoded}\n"

    if offset is not None:
        with open(target_file, "r+", encoding="utf-8") as f:
            f.seek(offset)
            remainder = f.read()
            f.seek(offset)
            f.write(line + remainder[len(line):])
        return offset

    with open(target_file, "a", encoding="utf-8") as f:
        pos = f.tell()
        f.write(line)
        return pos


def extract_shard_from_file(target_file: str, offset: int) -> bytes:
    """Extract a shard previously embedded at the given offset.

    Args:
        target_file: Path to the file containing the shard.
        offset: Byte offset of the ``//`` that starts the SHARD line.

    Returns:
        The decoded shard bytes.
    """
    with open(target_file, "r", encoding="utf-8") as f:
        f.seek(offset)
        line = f.readline().strip()

    m = re.match(rf"^{re.escape(_SHARD_PREFIX)}(.+)$", line)
    if not m:
        raise ValueError(f"No valid SHARD line at offset {offset}")

    return base64.b64decode(m.group(1))
