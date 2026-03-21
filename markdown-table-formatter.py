#!/usr/bin/env python3
"""Format markdown tables to align columns.

Usage:
    python markdown-table-formatter.py file1.md file2.md   # format in-place
    python markdown-table-formatter.py                     # stdin → stdout
"""

import re
import sys


def parse_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def is_separator_row(row):
    return all(re.match(r"^:?-+:?$", cell) for cell in row if cell)


def format_separator_cell(cell, width):
    left = cell.startswith(":")
    right = cell.endswith(":")
    dashes = width - left - right
    if dashes < 1:
        dashes = 1
    return (":" if left else "") + "-" * dashes + (":" if right else "")


def format_table(lines):
    rows = [parse_row(line) for line in lines]

    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]

    widths = [3] * ncols  # minimum 3 for separator dashes
    for row in rows:
        if is_separator_row(row):
            continue
        for j, cell in enumerate(row):
            widths[j] = max(widths[j], len(cell))

    result = []
    for row in rows:
        if is_separator_row(row):
            cells = [format_separator_cell(cell, widths[j]) for j, cell in enumerate(row)]
        else:
            cells = [cell.ljust(widths[j]) for j, cell in enumerate(row)]
        result.append("| " + " | ".join(cells) + " |")
    return result


def process(text):
    lines = text.splitlines()
    output = []
    table_lines = []

    for line in lines:
        if line.strip().startswith("|") and line.strip().endswith("|"):
            table_lines.append(line)
        else:
            if table_lines:
                output.extend(format_table(table_lines))
                table_lines = []
            output.append(line)

    if table_lines:
        output.extend(format_table(table_lines))

    # Preserve trailing newline
    result = "\n".join(output)
    if text.endswith("\n"):
        result += "\n"
    return result


def main():
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            with open(path, encoding="utf-8") as f:
                text = f.read()
            formatted = process(text)
            if formatted != text:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(formatted)
                print(f"formatted: {path}")
            else:
                print(f"no change: {path}")
    else:
        sys.stdout.write(process(sys.stdin.read()))


if __name__ == "__main__":
    main()
