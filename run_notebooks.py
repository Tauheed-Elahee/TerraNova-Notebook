#!/usr/bin/env python3
"""
run_notebooks.py — Execute Jupyter notebooks with papermill and export as HTML.

Each notebook is executed by papermill with its own directory as the working
directory (so relative paths such as data/ resolve correctly), output is written
to a temporary file, then converted to HTML via nbconvert with code cells hidden.

Results are written to output/<notebook-stem>.html (sibling of the notebook) by default.
Data files are read/written from data/ (sibling of the notebook) by default; override with
--data-dir to share a single data directory across all notebooks.

Usage:
    python3 run_notebooks.py notebook.ipynb [notebook2.ipynb ...]
    python3 run_notebooks.py --output-dir path/to/dir notebook.ipynb
    python3 run_notebooks.py --data-dir path/to/data notebook.ipynb

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

def run_notebook(path: Path, output_dir: Path | None, data_dir: Path | None) -> bool:
    """Execute a notebook with papermill and export it as HTML. Returns True on success."""
    resolved_output_dir = (output_dir or path.parent / "output").resolve()
    resolved_output_dir.mkdir(parents=True, exist_ok=True)
    out_html = resolved_output_dir / f"{path.stem}.html"

    with tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        print(f"\n[{path.name}]")

        cmd = ["papermill", str(path.resolve()), str(tmp_path)]
        if data_dir is not None:
            cmd += ["-p", "DATA_DIR", str(data_dir.resolve())]

        print(f"  papermill: executing...")
        result = subprocess.run(cmd, cwd=path.parent.resolve())
        if result.returncode != 0:
            print(f"  ERROR: papermill failed (see above)", file=sys.stderr)
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
        "--output-dir", type=Path, default=None,
        help="Directory to write HTML output (default: output/ next to each notebook)",
    )
    parser.add_argument(
        "--data-dir", type=Path, default=None,
        help="Data directory for all notebooks (default: data/ next to each notebook)",
    )
    args = parser.parse_args()

    for path in args.notebooks:
        if not path.exists():
            print(f"ERROR: {path} not found", file=sys.stderr)
            sys.exit(2)

    ok = True
    for path in args.notebooks:
        if not run_notebook(path, args.output_dir, args.data_dir):
            ok = False

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
