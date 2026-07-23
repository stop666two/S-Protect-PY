import hashlib
import hmac
import json
import zlib
from pathlib import Path

import blake3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305


ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "_runtime"
MODULES = {
    "main": "ad6365473630.pye",
    "_sprotect_helper": "29af4a2d774e.pye",
}


def select_shard(record):
    shards = [bytes.fromhex(record[f"k{i}"]) for i in range(1, 6)]
    combined = bytearray(32)
    for shard in shards:
        for i, value in enumerate(shard[:32]):
            combined[i] ^= value

    f1_ok = hashlib.sha256(combined).hexdigest()[5:13] == record["f1"]
    for shard in shards:
        f2_ok = blake3.blake3(shard).hexdigest()[3:11] == record["f2"]
        f3_ok = hmac.new(
            shard, b"S-Protect-v6-key-verify", hashlib.sha256
        ).hexdigest()[:8] == record["f3"]
        if f1_ok and f2_ok and f3_ok:
            return shard
    raise ValueError("No valid key shard")


def hash_stream(length, seed):
    result = bytearray()
    counter = 0
    while len(result) < length:
        result.extend(hashlib.sha256(seed + counter.to_bytes(4, "big")).digest())
        counter += 1
    return bytes(result[:length])


def decrypt(record, key):
    encrypted = bytes.fromhex(record["d"])
    data = AESGCM(key).decrypt(encrypted[:12], encrypted[12:], b"")
    stream = hash_stream(len(data), hashlib.sha256(key).digest())
    data = bytes(left ^ right for left, right in zip(data, stream))
    data = ChaCha20Poly1305(key).decrypt(data[:12], data[12:], b"")
    return zlib.decompress(data).decode("utf-8")


def main():
    records = {
        name: json.loads((RUNTIME / filename).read_text())
        for name, filename in MODULES.items()
    }
    shards = [select_shard(record) for record in records.values()]
    master_key = bytes(a ^ b for a, b in zip(*shards))

    for name, record in records.items():
        source = decrypt(record, master_key)
        destination = ROOT / ("final.py" if name == "main" else f"{name}.py")
        destination.write_text(source, encoding="utf-8")
        compile(source, str(destination), "exec")
        print(f"wrote {destination.name}: {len(source)} chars")


if __name__ == "__main__":
    main()