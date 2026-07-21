"""Decryption (testing/verification only)."""
from sprotect.crypto import decrypt_payload

def decrypt_file(data: bytes) -> tuple[str, str]:
    return decrypt_payload(data)
