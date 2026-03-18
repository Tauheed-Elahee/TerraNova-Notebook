#!/usr/bin/env python3
"""
fix_notebook_sources.py — Convert Jupyter notebook cell `source` fields
from a single string to an array of strings (the canonical nbformat).

Usage:
    python3 fix_notebook_sources.py notebook.ipynb [notebook2.ipynb ...]
    python3 fix_notebook_sources.py --check notebook.ipynb   # exit 1 if any need fixing
"""

import argparse
import json
import sys
from pathlib import Path


def split_source(source: str) -> list[str]:
    """Split a source string into lines, preserving trailing newlines on each line."""
    if not source:
        return []
    lines = source.splitlines(keepends=True)
    return lines


def fix_notebook(path: Path, check_only: bool) -> bool:
    """
    Returns True if the file was (or would be) modified.
    """
    try:
        text = path.read_text(encoding="utf-8")
        nb = json.loads(text)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR {path}: {e}", file=sys.stderr)
        return False

    cells = nb.get("cells", [])
    changed = False

    for i, cell in enumerate(cells):
        source = cell.get("source")
        if isinstance(source, str):
            cell["source"] = split_source(source)
            changed = True
            cell_id = cell.get("id", f"index {i}")
            print(f"  {'would fix' if check_only else 'fixed'} cell {cell_id!r} in {path}")

    if changed and not check_only:
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    return changed


EPILOG = """
examples:
  python3 fix_notebook_sources.py notebook.ipynb
      Fix a single notebook in place.

  python3 fix_notebook_sources.py *.ipynb
      Fix all notebooks in the current directory.

  python3 fix_notebook_sources.py --check *.ipynb
      Lint only — print offending cells and exit 1 if any are found,
      without modifying any files. Suitable for use in CI.

exit codes:
  0   No issues found (or all issues fixed)
  1   --check found at least one string source field
  2   A specified notebook path does not exist
"""


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("notebooks", nargs="+", type=Path, metavar="NOTEBOOK")
    parser.add_argument("--check", action="store_true", help="Report issues without modifying files; exit 1 if any found")
    args = parser.parse_args()

    any_changed = False
    for path in args.notebooks:
        if not path.exists():
            print(f"ERROR: {path} not found", file=sys.stderr)
            sys.exit(2)
        changed = fix_notebook(path, check_only=args.check)
        if changed:
            any_changed = True
            if not args.check:
                print(f"  wrote {path}")

    if args.check and any_changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
