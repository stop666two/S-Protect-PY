"""Tests for the index builder and truth-offset mask.

Covers IndexBuilder with mixed true/false/noise entries, the build
output structure, and the generate_truth_offset_mask helper.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

from sprotect.utils.index_builder import IndexBuilder, generate_truth_offset_mask


def test_index_builder() -> None:
    """IndexBuilder should produce correct counts and entry types."""
    builder = IndexBuilder(project_dir="/fake/project", shard_count=3, file_count=5)
    builder.add_true_entry("src/a.py", 100, 32)
    builder.add_true_entry("src/b.py", 200, 32)
    builder.add_false_entry("src/c.py", 300, 32)
    builder.add_noise_entries(3)

    result = builder.build()
    assert result["version"] == 1
    assert result["shard_count"] == 3
    assert result["file_count"] == 5
    assert len(result["entries"]) == 6

    real_count = sum(1 for e in result["entries"] if e["real"])
    assert real_count == 2

    false_count = sum(1 for e in result["entries"] if not e["real"])
    assert false_count == 4


def test_truth_offset_mask() -> None:
    """generate_truth_offset_mask should interleave real and fake offsets."""
    true_offsets = [100, 200, 300]
    masked = generate_truth_offset_mask(true_offsets)
    assert len(masked) == 6
    assert masked[0] == 100
    assert masked[2] == 200
    assert masked[4] == 300
    assert masked[1] != masked[0]
    assert masked[3] != masked[2]
    assert masked[5] != masked[4]
