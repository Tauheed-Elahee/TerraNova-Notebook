#!/usr/bin/env python3
"""
run_notebooks.py — Execute Jupyter notebooks with papermill and export as HTML.

Each notebook is executed in-place by papermill, then converted to HTML via
nbconvert. Results are written to notes/experiments/<notebook-stem>.html.

Usage:
    python3 run_notebooks.py notebook.ipynb [notebook2.ipynb ...]

exit codes:
  0   All notebooks succeeded
  1   One or more notebooks failed
  2   A specified notebook path does not exist
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

def run_notebook(path: Path, output_dir: Path) -> bool:
    """Execute a notebook with papermill and export it as HTML. Returns True on success."""
    out_html = output_dir / f"{path.stem}.html"

    with tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        print(f"\n[{path.name}]")

        print(f"  papermill: executing...")
        result = subprocess.run(
            ["papermill", str(path), str(tmp_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  ERROR: papermill failed", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return False

        print(f"  nbconvert: converting to HTML...")
        result = subprocess.run(
            [
                "jupyter", "nbconvert",
                "--to", "html",
                "--no-input",
                "--output", str(out_html),
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  ERROR: nbconvert failed", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return False

        print(f"  wrote {out_html}")
        return True

    finally:
        tmp_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("notebooks", nargs="+", type=Path, metavar="NOTEBOOK")
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path(__file__).parent / "notes" / "experiments",
        help="Directory to write HTML output (default: notes/experiments/)",
    )
    args = parser.parse_args()

    for path in args.notebooks:
        if not path.exists():
            print(f"ERROR: {path} not found", file=sys.stderr)
            sys.exit(2)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    ok = True
    for path in args.notebooks:
        if not run_notebook(path, args.output_dir):
            ok = False

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
