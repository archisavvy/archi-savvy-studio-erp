#!/usr/bin/env python3
"""Repeatable rebrand of the upstream OpenBusinessERP tree.

Archi Savvy Studio ERP is a modified version of OpenBusinessERP
(Copyright Artem Boiko / DataDrivenConstruction, AGPL-3.0-or-later).
The upstream trademark policy requires a modified version to carry its own
name and logo. This script applies that rename mechanically so it can be
re-run on every new upstream release (see docs/fork/UPDATING.md).

What it never touches:
  * licence, notice, copyright, contributor and trademark files;
  * any line carrying a copyright / SPDX / provenance marker;
  * the upstream changelog.

Run from the repository root:  python3 -I tools/rebrand/rebrand.py [--check]
The script is idempotent: a second run changes nothing.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

# ---- brand configuration -------------------------------------------------
PRODUCT = "Archi Savvy Studio ERP"      # shown to people
COMPACT = "ArchiSavvyStudioERP"         # file names, paths, identifiers
PUBLISHER = "Archi Savvy Studio"
NEW_REPO = "Fabsye/archi-savvy-studio-erp"
SIDECAR = "archisavvy-erp-server"
APP_ID = "com.archisavvy.studioerp"
DATA_DIR = ".archisavvy-erp"

UPSTREAM_REPO = "datadrivenconstruction/OpenBusinessERP"

# ---- protection ----------------------------------------------------------
PROTECTED_FILES = {
    "LICENSE", "backend/LICENSE", "NOTICE", "backend/NOTICE", "COPYRIGHT",
    "CLA.md", "TRADEMARK.md", "AUTHORS.md", "CONTRIBUTORS.md", "CHANGELOG.md",
    "CITATION.cff", ".github/CODEOWNERS",
}
PROTECTED_PREFIXES = ("docs/legal/", "tools/rebrand/", "docs/fork/")
PROTECTED_SUFFIXES = (".lock", "package-lock.json")
PROTECTED_LINE = re.compile(
    r"DDC-CWICR|Copyright|SPDX|OpenBusinessERP\s*[-—]\s*DataDrivenConstruction \(DDC\)"
    r"|[Bb]ased on OpenBusinessERP|rebrand:keep"
)

NAME = re.compile(r"OpenBusinessERP")
COMPACT_BEFORE = set("/\\_.@") | set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
WORD = re.compile(r"[A-Za-z0-9_]")


def _name_sub(line: str) -> str:
    def repl(m: re.Match[str]) -> str:
        before = line[m.start() - 1] if m.start() else ""
        before2 = line[m.start() - 2] if m.start() > 1 else ""
        after = line[m.end(): m.end() + 2]
        a0 = after[:1]
        a1 = after[1:2]
        compact = (
            before in COMPACT_BEFORE
            or (before == "-" and before2.isascii() and before2.isalnum())
            or bool(WORD.match(a0))
            or a0 in "/\\_@"
            or (a0 == "." and bool(WORD.match(a1)))
        )
        return COMPACT if compact else PRODUCT
    return NAME.sub(repl, line)


def transform_line(line: str) -> str:
    if PROTECTED_LINE.search(line):
        return line
    out = line
    out = out.replace("datadrivenconstruction.github.io/OpenBusinessERP", f"github.com/{NEW_REPO}")
    out = out.replace(UPSTREAM_REPO, NEW_REPO)
    out = out.replace("io.openbusinesserp.desktop", APP_ID)
    out = re.sub(r"openbusinesserp-server(?!\.spec)", SIDECAR, out)
    out = re.sub(r"(?<![A-Za-z0-9_])\.openestimate\b", DATA_DIR, out)
    out = _name_sub(out)
    return out


def is_protected(path: str) -> bool:
    return (
        path in PROTECTED_FILES
        or path.startswith(PROTECTED_PREFIXES)
        or path.endswith(PROTECTED_SUFFIXES)
    )


def tracked_files() -> list[str]:
    res = subprocess.run(["git", "ls-files", "-z"], capture_output=True, check=True)
    return [p for p in res.stdout.decode().split("\0") if p]


def patch_tauri_conf(root: Path) -> bool:
    path = root / "desktop/src-tauri/tauri.conf.json"
    if not path.exists():
        return False
    before = path.read_text(encoding="utf-8")
    conf = json.loads(before)
    conf["productName"] = PRODUCT
    conf["mainBinaryName"] = COMPACT
    conf["identifier"] = APP_ID
    conf["app"]["windows"][0]["title"] = PRODUCT
    conf["app"]["trayIcon"]["tooltip"] = PRODUCT
    b = conf["bundle"]
    b["publisher"] = PUBLISHER
    b["copyright"] = (
        "Copyright Archi Savvy Studio (modifications). Based on OpenBusinessERP, "
        "Copyright Artem Boiko / DataDrivenConstruction. Licensed under AGPL-3.0-or-later."
    )
    b["shortDescription"] = "ERP for architecture and design practices."
    b["longDescription"] = (
        f"{PRODUCT} is practice-management and ERP software for architecture and design "
        "studios: projects, clients, quotes, invoices, accounting, documents, drawings and "
        "cost planning. It runs fully local on an embedded database and works offline. "
        "It is based on OpenBusinessERP (open source) and licensed under AGPL-3.0."
    )
    after = json.dumps(conf, indent=2, ensure_ascii=False) + "\n"
    if after != before:
        path.write_text(after, encoding="utf-8")
        return True
    return False


def main() -> int:
    check = "--check" in sys.argv
    root = Path.cwd()
    changed: list[str] = []
    for rel in tracked_files():
        if is_protected(rel):
            continue
        p = root / rel
        if not p.is_file() or p.is_symlink():
            continue
        raw = p.read_bytes()
        if b"\0" in raw[:8192]:
            continue
        enc = "utf-8"
        try:
            text = raw.decode(enc)
        except UnicodeDecodeError:
            enc = "latin-1"
            text = raw.decode(enc)
        if ("OpenBusinessERP" not in text and "openbusinesserp" not in text
                and ".openestimate" not in text):
            continue
        new = "".join(transform_line(l) for l in text.splitlines(keepends=True))
        if new != text:
            changed.append(rel)
            if not check:
                p.write_bytes(new.encode(enc))
    if not check and patch_tauri_conf(root):
        if "desktop/src-tauri/tauri.conf.json" not in changed:
            changed.append("desktop/src-tauri/tauri.conf.json")
    print(f"{'would change' if check else 'changed'} {len(changed)} files")
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
