"""Seed pool - random seed values used by multiple modules.
Cross-references: crypto.mixer (interleave), utils.math_ops (fibonacci)"""
import os


SEED_POOL = {
    "alpha": os.urandom(8).hex(),
    "beta": str(os.urandom(4).hex()),
    "gamma": str(len(__file__)),
    "delta": str(abs(hash("sprotect-seed")) % 100000),
}
