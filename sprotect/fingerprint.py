"""Digital fingerprint tracking — hash reporting for traceability."""
from __future__ import annotations
import os, hashlib, json, threading, time
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError


def compute_fingerprint(runtime_dir: str) -> dict:
    """Compute SHA256 fingerprints of all .pye files."""
    fingerprints = {}
    for root, _, files in os.walk(runtime_dir):
        for f in sorted(files):
            if f.endswith(".pye"):
                fp = os.path.join(root, f)
                h = hashlib.sha256()
                with open(fp, "rb") as fh:
                    while True:
                        chunk = fh.read(65536)
                        if not chunk: break
                        h.update(chunk)
                rel = os.path.relpath(fp, runtime_dir).replace("\\", "/")
                fingerprints[rel] = h.hexdigest()
    return fingerprints


def check_integrity(runtime_dir: str, manifest: dict) -> list[str]:
    """Compare current .pye hashes against expected manifest. Returns anomalies."""
    current = compute_fingerprint(runtime_dir)
    anomalies = []
    for rel, expected in manifest.items():
        actual = current.get(rel)
        if actual is None:
            anomalies.append(f"MISSING:{rel}")
        elif actual != expected:
            anomalies.append(f"MODIFIED:{rel}")
    extra = set(current) - set(manifest)
    for rel in extra:
        anomalies.append(f"EXTRA:{rel}")
    return anomalies


def report_fingerprint(server_url: str, batch_id: str, runtime_dir: str,
                       customer_id: str = "", timeout: float = 3.0) -> bool:
    """Compute and report fingerprints to remote server."""
    try:
        fp = compute_fingerprint(runtime_dir)
        payload = json.dumps({
            "batch_id": batch_id,
            "customer_id": customer_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "fingerprints": fp,
            "hostname": os.environ.get("COMPUTERNAME", os.environ.get("HOSTNAME", "")),
            "username": os.environ.get("USERNAME", os.environ.get("USER", "")),
        }).encode()
        req = Request(server_url, data=payload,
                      headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except (URLError, OSError, Exception):
        return False


def start_background_reporting(server_url: str, batch_id: str, runtime_dir: str,
                               interval_hours: int = 24, customer_id: str = "") -> threading.Thread:
    """Start background thread that periodically reports fingerprints."""
    def _loop():
        while True:
            try:
                report_fingerprint(server_url, batch_id, runtime_dir, customer_id)
            except Exception:
                pass
            time.sleep(interval_hours * 3600)
    t = threading.Thread(target=_loop, daemon=True)
    t.start()
    return t
