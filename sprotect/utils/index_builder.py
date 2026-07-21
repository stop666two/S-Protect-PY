"""True/false index builder for obfuscated shard metadata.

Builds an index that mixes real shard locations with decoy (false)
entries and noise, making it harder for an attacker to identify
which files carry the real shards.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import copy
import random
from typing import Any


class IndexBuilder:
    """Builds a mixed index of real, false, and noise shard entries.

    Entries are stored as dicts with keys: file, offset, length, real.
    Real entries point to files that actually contain shards; false
    and noise entries are decoys.
    """

    def __init__(self, project_dir: str, shard_count: int, file_count: int) -> None:
        """Initialize the IndexBuilder.

        Args:
            project_dir: Root directory of the project being indexed.
            shard_count: Number of key shards in the system.
            file_count: Total number of files in the project.
        """
        self.project_dir = project_dir
        self.shard_count = shard_count
        self.file_count = file_count
        self._entries: list[dict[str, Any]] = []

    def add_true_entry(self, file_rel: str, offset: int, length: int) -> None:
        """Add a real shard entry.

        Args:
            file_rel: Relative file path from project root.
            offset: Byte offset of the SHARD comment in the file.
            length: Length of the shard data in bytes.
        """
        self._entries.append({
            "file": file_rel,
            "offset": offset,
            "length": length,
            "real": True,
        })

    def add_false_entry(self, file_rel: str, offset: int, length: int) -> None:
        """Add a decoy (false) shard entry.

        Args:
            file_rel: Relative file path from project root.
            offset: Byte offset in the file.
            length: Length value for the entry.
        """
        self._entries.append({
            "file": file_rel,
            "offset": offset,
            "length": length,
            "real": False,
        })

    def add_noise_entries(self, count: int) -> None:
        """Add *count* randomly generated noise entries.

        Noise entries have random file names, offsets, and lengths,
        all marked as ``real: False``.

        Args:
            count: Number of noise entries to generate.
        """
        for _ in range(count):
            fake_file = f"_internal/noise_{random.randint(1000, 9999)}.dat"
            self._entries.append({
                "file": fake_file,
                "offset": random.randint(0, 65535),
                "length": random.randint(16, 256),
                "real": False,
            })

    def build(self) -> dict[str, Any]:
        """Build and return the final index structure.

        Returns:
            A dict with keys ``version``, ``shard_count``,
            ``file_count``, and ``entries`` (a list of entry dicts).
        """
        return {
            "version": 1,
            "shard_count": self.shard_count,
            "file_count": self.file_count,
            "entries": copy.deepcopy(self._entries),
        }


def generate_truth_offset_mask(true_offsets: list[int]) -> list[int]:
    """Generate a mixed list of true and fake offsets.

    Each true offset is followed by a random fake offset, creating
    a 1:1 true/false pattern that obscures the real locations.

    Args:
        true_offsets: The real byte offsets to protect.

    Returns:
        A list where true and decoy offsets alternate.
    """
    result: list[int] = []
    for off in true_offsets:
        result.append(off)
        fake = off + random.randint(10, 100)
        result.append(fake)
    return result
