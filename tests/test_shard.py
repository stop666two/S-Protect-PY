"""Tests for the key sharding (shard.py) module.

Covers split/reconstruct round-trip, embed/extract round-trip,
shard count validation, and data integrity.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import os

import pytest

from sprotect.utils.shard import (
    embed_shard_into_file,
    extract_shard_from_file,
    reconstruct_key,
    split_key,
)

_TEST_TEMP = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_test_temp"
)
os.makedirs(_TEST_TEMP, exist_ok=True)


def _tmp_path(name: str) -> str:
    return os.path.join(_TEST_TEMP, name)


def test_split_and_reconstruct() -> None:
    """3-shard split + XOR reconstruction should return the original key."""
    key = b"my-secret-key-32bytes!!"
    shards = split_key(key, 3)
    assert len(shards) == 3
    for s in shards:
        assert len(s) == len(key)
    recovered = reconstruct_key(shards)
    assert recovered == key


def test_embed_and_extract() -> None:
    """Embed a shard into a file and extract it at the returned offset."""
    file_path = _tmp_path("_test_shard_embed.txt")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("line1\nline2\n")

        shard = b"\x01\x02\x03\x04\x05sharddata"
        offset = embed_shard_into_file(file_path, shard)
        assert offset >= 0

        extracted = extract_shard_from_file(file_path, offset)
        assert extracted == shard
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def test_shard_count_validation() -> None:
    """split_key must raise ValueError when shard_count is 1."""
    with pytest.raises(ValueError, match="shard_count must be >= 2"):
        split_key(b"test-key-12345", 1)


def test_split_key_integrity() -> None:
    """Reconstructed key must match the original for various key lengths."""
    original = os.urandom(32)
    shards = split_key(original, 5)
    recovered = reconstruct_key(shards)
    assert recovered == original


def test_embed_at_existing_offset() -> None:
    """Embedding at an existing offset should overwrite that line."""
    file_path = _tmp_path("_test_shard_overwrite.txt")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("first line\n")

        shard1 = b"aaaa"
        offset = embed_shard_into_file(file_path, shard1)
        assert extract_shard_from_file(file_path, offset) == shard1

        shard2 = b"bbbb"
        embed_shard_into_file(file_path, shard2, offset=offset)
        assert extract_shard_from_file(file_path, offset) == shard2
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
