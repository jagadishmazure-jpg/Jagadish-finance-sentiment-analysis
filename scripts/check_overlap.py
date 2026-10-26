"""8-word overlap check: repo docs vs a source text file.

Usage:
    python3 scripts/check_overlap.py --source /path/to/source.txt \
        --root /path/to/repo

Normalises both sides (lowercase, non-alphanumerics to spaces), builds
every consecutive 8-word window from the source, and reports any window
that appears verbatim in a repo Markdown file. Target: 0 hits.
The source file itself is never copied into the repo.
"""

import argparse
import re
from pathlib import Path

_WORD = re.compile(r"[a-z0-9]+")


def windows(text, n=8):
    tokens = _WORD.findall(text.lower())
    return {" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    source_windows = windows(Path(args.source).read_text(errors="ignore"))
    hits = []
    for md in sorted(Path(args.root).rglob("*.md")):
        normalised = " ".join(_WORD.findall(md.read_text(errors="ignore").lower()))
        for window in sorted(source_windows):
            if window in normalised:
                hits.append((str(md), window))
    print(f"source 8-word windows: {len(source_windows)}")
    print(f"hits: {len(hits)}")
    for path, window in hits:
        print(f"  {path}: {window!r}")
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
