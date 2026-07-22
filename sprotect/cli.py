"""S-Protect-PY CLI."""

from __future__ import annotations
import argparse, sys, os, json5
from pathlib import Path
from sprotect import __version__
from sprotect.config import load_config, gen_default
from sprotect.encrypt import build as build_project
from sprotect.backup import backup


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sprotect", description="S-Protect-PY: Python code protection toolkit.")
    s = p.add_subparsers(dest="cmd", required=True)

    b = s.add_parser("build", help="Build encrypted project (project/ -> output/)")
    b.add_argument("--project", default="./project", help="Source project directory")
    b.add_argument("--output", default="./output", help="Output directory")
    b.add_argument("-c", "--config", help="Path to sprotect.json5")
    b.add_argument("--clean", action="store_true", help="Auto-clean output directory before build")
    b.add_argument("--watch", action="store_true", help="Watch project files and auto-rebuild on change")

    e = s.add_parser("encrypt", help="Encrypt individual files")
    e.add_argument("files", nargs="+")
    e.add_argument("-c", "--config")

    c = s.add_parser("config", help="Manage configuration")
    cs = c.add_subparsers(dest="ca", required=True)
    cs.add_parser("init", help="Generate default sprotect.json5")
    cs.add_parser("show", help="Show current config")

    i = s.add_parser("init", help="Initialize project/ and output/ directories")
    i.add_argument("--project", default="./project", help="Source directory")
    i.add_argument("--output", default="./output", help="Output directory")

    w = s.add_parser("watermark", help="Extract or verify watermark from .pye files")
    ws = w.add_subparsers(dest="wa", required=True)
    we = ws.add_parser("extract", help="Extract watermark from a .pye file")
    we.add_argument("file", help="Path to .pye file")
    we.add_argument("--key", help="Secret key for authenticity verification")
    wv = ws.add_parser("verify", help="Verify watermark signature + authenticity")
    wv.add_argument("file", help="Path to .pye file")
    wv.add_argument("--key", help="Secret key for authenticity verification")
    wl = ws.add_parser("list", help="List watermarks in a directory")
    wl.add_argument("dir", default="./output/_runtime", nargs="?", help="Directory containing .pye files")

    pk = s.add_parser("pack", help="Pack encrypted output into single exe (requires PyInstaller)")
    pk.add_argument("--output", default="./output", help="Output directory (the one from sprotect build)")
    pk.add_argument("--onefile", action="store_true", default=True, help="Single exe file (default)")
    pk.add_argument("--onedir", action="store_true", help="Directory with exe + dependencies")
    pk.add_argument("--console", action="store_true", default=True, help="Show console window")
    pk.add_argument("--noconsole", action="store_true", help="Hide console window")
    pk.add_argument("--icon", help="Custom .exe icon")

    s.add_parser("version", help="Show version")

    ru = s.add_parser("run", help="Run an encrypted project")
    ru.add_argument("--dir", default="./output", help="Output directory (default: ./output)")

    return p


def main(argv: list[str] | None = None) -> int:
    p = _parser()
    a = p.parse_args(argv)

    if a.cmd == "watermark":
        from sprotect.watermark import extract_watermark, verify_watermark
        if a.wa == "extract":
            key = getattr(a, "key", "")
            wm = extract_watermark(a.file, key)
            if wm:
                print(f"Batch ID:     {wm.get('bid', 'N/A')}")
                print(f"Timestamp:    {wm.get('ts', 'N/A')}")
                print(f"Signature:    {wm.get('sig', 'N/A')} {'OK' if wm.get('sig_ok') else 'BAD'}")
                if key:
                    print(f"Authenticity: {wm.get('auth', 'N/A')} {'OK' if wm.get('auth_ok') else 'BAD'}")
                print(f"Type:         {wm.get('t', 'N/A')}")
            else:
                print("No watermark found.")
                return 1
            return 0
        elif a.wa == "verify":
            key = getattr(a, "key", "")
            ok = verify_watermark(a.file, key)
            print(f"Watermark: {'VALID' if ok else 'INVALID or not found'}")
            return 0 if ok else 1
        elif a.wa == "list":
            import glob
            path = a.dir
            if not os.path.isdir(path):
                print(f"Directory not found: {path}")
                return 1
            files = sorted(glob.glob(os.path.join(path, "*.pye")))
            found = 0
            for f in files:
                wm = extract_watermark(f)
                if wm:
                    fn = os.path.basename(f)
                    bid = wm.get("bid", "?")
                    ts = wm.get("ts", "?")[:19]
                    ok = "[OK]" if wm.get("sig_ok") else "[BAD]"
                    print(f"  {fn:30s} bid={bid:20s} ts={ts} {ok}")
                    found += 1
            print(f"\n{found} watermarked files found in {path}")
            return 0

    if a.cmd == "version":
        print(f"S-Protect-PY v{__version__}"); return 0

    if a.cmd == "init":
        for d in [a.project, a.output]:
            p = Path(d)
            p.mkdir(parents=True, exist_ok=True)
            (p / ".gitkeep").touch()
        print(f"Initialized:")
        print(f"  Source: {Path(a.project).resolve()}")
        print(f"  Output: {Path(a.output).resolve()}")
        if not Path("sprotect.json5").exists():
            from sprotect.config import gen_default
            gen_default("sprotect.json5")
            print(f"  Config: {Path('sprotect.json5').resolve()}")
        return 0

    if a.cmd == "config":
        if a.ca == "init":
            d = gen_default("sprotect.json5")
            print(f"Default config generated: {d.resolve()}"); return 0
        cfg = load_config()
        print(json5.dumps(cfg, indent=2, default=str)); return 0

    cfg = load_config(getattr(a, "config", None))

    if a.cmd == "pack":
        from sprotect.pack import pack as do_pack
        out = str(Path(a.output).resolve())
        pcfg = cfg.pack
        if hasattr(a, "onefile") and a.onefile: pcfg.onefile = True
        if hasattr(a, "onedir") and a.onedir: pcfg.onefile = False
        if hasattr(a, "noconsole") and a.noconsole: pcfg.console = False
        if hasattr(a, "icon") and a.icon: pcfg.icon = a.icon
        exe = do_pack(out, pcfg)
        return 0 if exe else 1

    if a.cmd == "build":
        proj = str(Path(a.project).resolve())
        out = str(Path(a.output).resolve())
        if not Path(proj).is_dir():
            print(f"Error: project directory not found: {proj}", file=sys.stderr); return 1
        if getattr(a, "clean", False) and Path(out).is_dir():
            import shutil as _su, time as _tm
            for _ in range(5):
                any_left = False
                for p in list(Path(out).iterdir()):
                    try:
                        if p.is_dir():
                            _su.rmtree(p, ignore_errors=True)
                        else:
                            p.unlink(missing_ok=True)
                    except: pass
                    if p.exists():
                        any_left = True
                if not any_left:
                    break
                _tm.sleep(0.5)
        if cfg.encrypt.backup: backup(proj)
        build_project(proj, out, cfg)
        if not Path(os.path.join(out, "main.py")).is_file():
            print(f"  Build failed: output incomplete", file=sys.stderr); return 1
        print(f"Project '{cfg.project.name}' encrypted.")
        print(f"  Output: {out}")
        print(f"  Entry:  {cfg.project.entry}")
        if cfg.pack.enabled:
            from sprotect.pack import pack as do_pack
            exe = do_pack(out, cfg.pack)
            if exe:
                print(f"  Packed: {exe}")
        if getattr(a, "watch", False):
            import time
            py_files = sorted(p for p in Path(proj).rglob("*.py") if not any(
                d in p.parts for d in ("__pycache__", ".git", "_backup", "_runtime")))
            mtimes = {str(p): os.path.getmtime(p) for p in py_files}
            print(f"  Watching {len(py_files)} files...")
            try:
                while True:
                    time.sleep(1)
                    for p in py_files:
                        fp = str(p)
                        mt = os.path.getmtime(fp)
                        if mt != mtimes[fp]:
                            print(f"\n  Change detected: {p.name}")
                            mtimes[fp] = mt
                            build_project(proj, out, cfg)
                            print(f"  Rebuild done. Watching...")
                            break
            except KeyboardInterrupt:
                print("\n  Watch stopped.")
        return 0

    if a.cmd == "run":
        run_dir = str(Path(a.dir).resolve())
        entry = os.path.join(run_dir, cfg.project.entry)
        if not os.path.isfile(entry):
            print(f"Entry not found: {entry}", file=sys.stderr); return 1
        env = os.environ.copy()
        env_file = os.path.join(run_dir, ".env")
        if os.path.isfile(env_file):
            for line in open(env_file, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip("\"'")
        import subprocess
        r = subprocess.run([sys.executable, entry], cwd=run_dir, env=env)
        return r.returncode

    if a.cmd == "encrypt":
        for f in a.files:
            if not Path(f).exists():
                print(f"Error: {f} not found", file=sys.stderr); return 1
        for f in a.files:
            pye = f.replace(".py", ".pye")
            from sprotect.crypto import encrypt_payload as ep
            from sprotect.obfuscate import Obfuscator
            src = open(f, encoding="utf-8").read()
            if cfg.obfuscate.level.value >= 1:
                src = Obfuscator(cfg.obfuscate).obfuscate(src)
            open(pye, "wb").write(ep(src.encode(), cfg.encrypt.algorithm))
            print(f"  Encrypted: {pye}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
