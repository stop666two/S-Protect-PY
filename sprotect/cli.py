# CLI DISPATCHER: command routing layer v2
# ENTRY: argparse subcommand tree

"""S-Protect-PY CLI."""

from __future__ import annotations
import argparse, sys, os, json5
from pathlib import Path
from sprotect import __version__
from sprotect.config import load_config, gen_default
from sprotect.encrypt import build as build_project
from sprotect.backup import backup


def _build_arg_tree() -> argparse.ArgumentParser:
    _ap = argparse.ArgumentParser(prog="sprotect", description="S-Protect-PY: Python code protection toolkit.")
    _sub_cmds = _ap.add_subparsers(dest="cmd", required=True)

    _bp_build = _sub_cmds.add_parser("build", help="Build encrypted project (project/ -> output/)")
    _bp_build.add_argument("--project", default="./project", help="Source project directory")
    _bp_build.add_argument("--output", default="./output", help="Output directory")
    _bp_build.add_argument("-c", "--config", help="Path to sprotect.json5")
    _bp_build.add_argument("--clean", action="store_true", help="Auto-clean output directory before build")
    _bp_build.add_argument("--watch", action="store_true", help="Watch project files and auto-rebuild on change")

    _bp_encrypt = _sub_cmds.add_parser("encrypt", help="Encrypt individual files")
    _bp_encrypt.add_argument("files", nargs="+")
    _bp_encrypt.add_argument("-c", "--config")

    _bp_config = _sub_cmds.add_parser("config", help="Manage configuration")
    _csub = _bp_config.add_subparsers(dest="ca", required=True)
    _csub.add_parser("init", help="Generate default sprotect.json5")
    _csub.add_parser("show", help="Show current config")

    _bp_init = _sub_cmds.add_parser("init", help="Initialize project/ and output/ directories")
    _bp_init.add_argument("--project", default="./project", help="Source directory")
    _bp_init.add_argument("--output", default="./output", help="Output directory")

    _bp_watermark = _sub_cmds.add_parser("watermark", help="Extract or verify watermark from .pye files")
    _wsub = _bp_watermark.add_subparsers(dest="wa", required=True)
    _bp_extract = _wsub.add_parser("extract", help="Extract watermark from a .pye file")
    _bp_extract.add_argument("file", help="Path to .pye file")
    _bp_extract.add_argument("--key", help="Secret key for authenticity verification")
    _bp_verify = _wsub.add_parser("verify", help="Verify watermark signature + authenticity")
    _bp_verify.add_argument("file", help="Path to .pye file")
    _bp_verify.add_argument("--key", help="Secret key for authenticity verification")
    _bp_list = _wsub.add_parser("list", help="List watermarks in a directory")
    _bp_list.add_argument("dir", default="./output/_runtime", nargs="?", help="Directory containing .pye files")

    _bp_pack = _sub_cmds.add_parser("pack", help="Pack encrypted output into single exe (requires PyInstaller)")
    _bp_pack.add_argument("--output", default="./output", help="Output directory (the one from sprotect build)")
    _bp_pack.add_argument("--onefile", action="store_true", default=True, help="Single exe file (default)")
    _bp_pack.add_argument("--onedir", action="store_true", help="Directory with exe + dependencies")
    _bp_pack.add_argument("--console", action="store_true", default=True, help="Show console window")
    _bp_pack.add_argument("--noconsole", action="store_true", help="Hide console window")
    _bp_pack.add_argument("--icon", help="Custom .exe icon")

    _sub_cmds.add_parser("version", help="Show version")

    _bp_run = _sub_cmds.add_parser("run", help="Run an encrypted project")
    _bp_run.add_argument("--dir", default="./output", help="Output directory (default: ./output)")

    return _ap


def main(argv: list[str] | None = None) -> int:
    _ap = _build_arg_tree()
    _args = _ap.parse_args(argv)

    if _args.cmd == "watermark":
        from sprotect.watermark import extract_watermark, verify_watermark
        if _args.wa == "extract":
            key = getattr(_args, "key", "")
            wm = extract_watermark(_args.file, key)
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
        elif _args.wa == "verify":
            key = getattr(_args, "key", "")
            ok = verify_watermark(_args.file, key)
            print(f"Watermark: {'VALID' if ok else 'INVALID or not found'}")
            return 0 if ok else 1
        elif _args.wa == "list":
            import glob
            path = _args.dir
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

    if _args.cmd == "version":
        print(f"S-Protect-PY v{__version__}"); return 0

    if _args.cmd == "init":
        for d in [_args.project, _args.output]:
            p = Path(d)
            p.mkdir(parents=True, exist_ok=True)
            (p / ".gitkeep").touch()
        print(f"Initialized:")
        print(f"  Source: {Path(_args.project).resolve()}")
        print(f"  Output: {Path(_args.output).resolve()}")
        if not Path("sprotect.json5").exists():
            from sprotect.config import gen_default
            gen_default("sprotect.json5")
            print(f"  Config: {Path('sprotect.json5').resolve()}")
        return 0

    if _args.cmd == "config":
        if _args.ca == "init":
            d = gen_default("sprotect.json5")
            print(f"Default config generated: {d.resolve()}"); return 0
        cfg = load_config()
        print(json5.dumps(cfg, indent=2, default=str)); return 0

    cfg = load_config(getattr(_args, "config", None))

    if _args.cmd == "pack":
        from sprotect.pack import pack as do_pack
        _out_path = str(Path(_args.output).resolve())
        _pack_settings = cfg.pack
        if hasattr(_args, "onefile") and _args.onefile: _pack_settings.onefile = True
        if hasattr(_args, "onedir") and _args.onedir: _pack_settings.onefile = False
        if hasattr(_args, "noconsole") and _args.noconsole: _pack_settings.console = False
        if hasattr(_args, "icon") and _args.icon: _pack_settings.icon = _args.icon
        exe = do_pack(_out_path, _pack_settings)
        return 0 if exe else 1

    if _args.cmd == "build":
        _src_path = str(Path(_args.project).resolve())
        _out_path = str(Path(_args.output).resolve())
        if not Path(_src_path).is_dir():
            print(f"Error: project directory not found: {_src_path}", file=sys.stderr); return 1
        if getattr(_args, "clean", False) and Path(_out_path).is_dir():
            import shutil as _su, time as _tm
            for _ in range(5):
                try:
                    for p in list(Path(_out_path).iterdir()):
                        if p.is_dir():
                            _su.rmtree(p, ignore_errors=True)
                        else:
                            p.unlink(missing_ok=True)
                    if not any(Path(_out_path).iterdir()):
                        break
                except (FileNotFoundError, PermissionError):
                    pass
                _tm.sleep(0.5)
        if cfg.encrypt.backup: backup(_src_path)
        build_project(_src_path, _out_path, cfg)
        entry_name = cfg.project.entry
        if not Path(os.path.join(_out_path, entry_name)).is_file():
            print(f"  Build failed: {entry_name} not generated", file=sys.stderr); return 1
        print(f"Project '{cfg.project.name}' encrypted.")
        print(f"  Output: {_out_path}")
        print(f"  Entry:  {cfg.project.entry}")
        if cfg.pack.enabled:
            from sprotect.pack import pack as do_pack
            exe = do_pack(_out_path, cfg.pack)
            if exe:
                print(f"  Packed: {exe}")
        if getattr(_args, "watch", False):
            import time
            py_files = sorted(p for p in Path(_src_path).rglob("*.py") if not any(
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
                            build_project(_src_path, _out_path, cfg)
                            print(f"  Rebuild done. Watching...")
                            break
            except KeyboardInterrupt:
                print("\n  Watch stopped.")
        return 0

    if _args.cmd == "run":
        run_dir = str(Path(_args.dir).resolve())
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
        if "PYTHONIOENCODING" not in env:
            env["PYTHONIOENCODING"] = "utf-8"
        _run_args = [sys.executable, entry]
        if cfg.dual_process.enabled:
            _run_args.append("--dual")
        r = subprocess.run(_run_args, cwd=run_dir, env=env)
        return r.returncode

    if _args.cmd == "encrypt":
        for f in _args.files:
            if not Path(f).exists():
                print(f"Error: {f} not found", file=sys.stderr); return 1
        for f in _args.files:
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
