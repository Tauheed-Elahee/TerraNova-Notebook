#!/usr/bin/env python3
"""
run_notebooks.py — Execute Jupyter notebooks with papermill and export as HTML.

Each notebook is executed by papermill with its own directory as the working
directory (so relative paths such as data/ resolve correctly), output is written
to a temporary file, then converted to HTML via nbconvert with code cells hidden.

Results are written to output/notebooks/<notebook-stem>.ipynb and output/html/<notebook-stem>.html
(sibling of the notebook) by default.
Data files are read/written from data/ (sibling of the notebook) by default; override with
--data-dir to share a single data directory across all notebooks.

Use --workspace-dir to set a common parent for data/, output/, and log/ at once.
Explicit --data-dir, --output-dir, or --log-dir take precedence over --workspace-dir.

Usage:
    python3 run_notebooks.py notebook.ipynb [notebook2.ipynb ...]
    python3 run_notebooks.py --output-dir path/to/dir notebook.ipynb
    python3 run_notebooks.py --data-dir path/to/data notebook.ipynb
    python3 run_notebooks.py --log-dir path/to/log notebook.ipynb
    python3 run_notebooks.py --workspace-dir path/to/ws notebook.ipynb
    python3 run_notebooks.py --workspace-dir path/to/ws --verbose notebook.ipynb

exit codes:
  0   All notebooks succeeded
  1   One or more notebooks failed
  2   A specified notebook path does not exist
"""

import argparse
import subprocess
import sys
import threading
from pathlib import Path


def _tee_stream(source, *destinations):
    """Read lines from source and write to all destinations."""
    for line in source:
        for dest in destinations:
            dest.write(line)
            dest.flush()


def _run(cmd, cwd, log_file, verbose):
    """Run a command, teeing output to log_file and terminal if verbose."""
    if log_file is None or not verbose:
        # No log file: inherit terminal. Log file without verbose: redirect only.
        return subprocess.run(cmd, cwd=cwd, stdout=log_file, stderr=log_file)
    # verbose + log: tee stdout+stderr to both terminal and log file
    proc = subprocess.Popen(
        cmd, cwd=cwd,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True,
    )
    t = threading.Thread(target=_tee_stream, args=(proc.stdout, sys.stdout, log_file))
    t.start()
    proc.wait()
    t.join()
    return proc


def run_notebook(path: Path, output_dir: Path | None, data_dir: Path | None, log_dir: Path | None, verbose: bool) -> bool:
    """Execute a notebook with papermill and export it as HTML. Returns True on success."""
    resolved_output_dir = (output_dir or path.parent / "output").resolve()
    nb_dir   = resolved_output_dir / "notebooks"
    html_dir = resolved_output_dir / "html"
    nb_dir.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)

    out_nb   = nb_dir   / f"{path.stem}.ipynb"
    out_html = html_dir / f"{path.stem}.html"

    print(f"\n[{path.name}]")

    log_file = None
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / f"{path.stem}.log"
        log_file = open(log_path, "w")
        print(f"  log: {log_path}")

    try:
        cmd = ["papermill", "--log-output", str(path.resolve()), str(out_nb)]
        if data_dir is not None:
            cmd += ["-p", "DATA_DIR", str(data_dir.resolve())]

        print(f"  papermill: executing...")
        result = _run(cmd, path.parent.resolve(), log_file, verbose)
        if result.returncode != 0:
            print(f"  ERROR: papermill failed (see {'log' if log_file else 'above'})", file=sys.stderr)
            return False

        print(f"  nbconvert: converting to HTML...")
        result = _run(
            [
                "jupyter", "nbconvert",
                "--to", "html",
                "--no-input",
                "--output", str(out_html),
                str(out_nb),
            ],
            path.parent.resolve(),
            log_file,
            verbose,
        )
        if result.returncode != 0:
            print(f"  ERROR: nbconvert failed (see {'log' if log_file else 'above'})", file=sys.stderr)
            return False

    finally:
        if log_file:
            log_file.close()

    print(f"  wrote {out_nb}")
    print(f"  wrote {out_html}")
    return True


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
    parser.add_argument(
        "--log-dir", type=Path, default=None,
        help="Directory to write per-notebook log files (default: no log file)",
    )
    parser.add_argument(
        "--workspace-dir", type=Path, default=None,
        help="Common parent for data/, output/, and log/ (shorthand for --data-dir <ws>/data --output-dir <ws>/output --log-dir <ws>/log)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Stream papermill and nbconvert output to both terminal and log file "
             "(only meaningful with --log-dir or --workspace-dir)",
    )
    args = parser.parse_args()

    for attr in ("workspace_dir", "data_dir", "output_dir", "log_dir"):
        if given_path := getattr(args, attr):
            setattr(args, attr, given_path.resolve())

    if workspace := args.workspace_dir:
        args.data_dir   = args.data_dir   or workspace / "data"
        args.output_dir = args.output_dir or workspace / "output"
        args.log_dir    = args.log_dir    or workspace / "log"

    for path in args.notebooks:
        if not path.exists():
            print(f"ERROR: {path} not found", file=sys.stderr)
            sys.exit(2)

    ok = True
    for path in args.notebooks:
        if not run_notebook(path, args.output_dir, args.data_dir, args.log_dir, args.verbose):
            ok = False

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
