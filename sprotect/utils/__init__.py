"""Utility modules for S-Protect-PY."""

from sprotect.utils.random_gen import RandomNameGenerator
from sprotect.utils.shard import (
    split_key,
    reconstruct_key,
    embed_shard_into_file,
    extract_shard_from_file,
)
from sprotect.utils.sign import (
    sign_file,
    verify_file_signature,
    build_chain_signatures,
)
from sprotect.utils.index_builder import IndexBuilder, generate_truth_offset_mask

__all__ = [
    "RandomNameGenerator",
    "split_key",
    "reconstruct_key",
    "embed_shard_into_file",
    "extract_shard_from_file",
    "sign_file",
    "verify_file_signature",
    "build_chain_signatures",
    "IndexBuilder",
    "generate_truth_offset_mask",
]
