"""Runtime shard collector and private-key reconstructor.

Walks the runtime directory, collects shards embedded in files
according to the index, filters for real entries only, and XOR-
reconstructs the original private key.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import os
from typing import Any

from sprotect.utils.shard import extract_shard_from_file, reconstruct_key


class ShardReconstructor:
    """Collects embedded shards from runtime files and reconstructs the key.

    Uses the index metadata to locate SHARD comments in project files,
    extracts only the entries marked ``real: True``, and XORs them
    back into the original private key.
    """

    def __init__(self, runtime_dir: str, index_data: dict[str, Any]) -> None:
        """Initialize with the runtime directory and parsed index.

        Args:
            runtime_dir: Path to the ``_runtime`` directory.
            index_data: The decoded index dict (from index_builder.build()).
        """
        self.runtime_dir = runtime_dir
        self.index_data = index_data

    def collect_shards(self) -> list[bytes]:
        """Collect all shards from files marked as real in the index.

        Only entries with ``real: True`` are collected; decoy and
        noise entries are ignored.

        Returns:
            A list of extracted shard byte strings, in the order they
            appear in the index entries.
        """
        shards: list[bytes] = []
        for entry in self.index_data.get("entries", []):
            if not entry.get("real"):
                continue
            file_path = os.path.join(self.runtime_dir, entry["file"])
            shard = extract_shard_from_file(file_path, entry["offset"])
            shards.append(shard)
        return shards

    def reconstruct_private_key(self) -> bytes:
        """Reconstruct the private key from all collected shards.

        Returns:
            The original private key bytes.

        Raises:
            ValueError: If fewer than 2 shards are collected.
        """
        shards = self.collect_shards()
        if len(shards) < 2:
            raise ValueError(
                f"Need at least 2 shards to reconstruct, found {len(shards)}"
            )
        return reconstruct_key(shards)
