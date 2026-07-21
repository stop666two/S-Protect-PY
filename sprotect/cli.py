"""S-Protect-PY CLI."""

from __future__ import annotations
import argparse, sys, json5
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

    s.add_parser("version", help="Show version")
    return p


def main(argv: list[str] | None = None) -> int:
    p = _parser()
    a = p.parse_args(argv)

    if a.cmd == "version":
        print(f"S-Protect-PY v{__version__}"); return 0

    if a.cmd == "init":
        import os
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

    if a.cmd == "build":
        proj = str(Path(a.project).resolve())
        out = str(Path(a.output).resolve())
        if not Path(proj).is_dir():
            print(f"Error: project directory not found: {proj}", file=sys.stderr); return 1
        if cfg.encrypt.backup: backup(proj)
        build_project(proj, out, cfg)
        print(f"Project '{cfg.project.name}' encrypted.")
        print(f"  Output: {out}")
        print(f"  Entry:  {cfg.project.entry}")
        return 0

    if a.cmd == "encrypt":
        from sprotect.encrypt import encrypt_file as ef
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
