"""Command-line interface for mdr."""

import argparse
import sys
from pathlib import Path

from mdr.server import serve


def main():
    parser = argparse.ArgumentParser(
        prog="mdr",
        description="Lightweight markdown reader - renders markdown in the browser",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Markdown file or directory to serve (default: current directory)",
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=0,
        help="Port to serve on (default: random free port)",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Don't automatically open browser",
    )

    args = parser.parse_args()
    path = Path(args.path).resolve()

    if not path.exists():
        print(f"mdr: error: {args.path} does not exist", file=sys.stderr)
        sys.exit(1)

    if path.is_file():
        if path.suffix.lower() != ".md":
            print(f"mdr: error: {args.path} is not a markdown file", file=sys.stderr)
            sys.exit(1)
        mode = "file"
    elif path.is_dir():
        mode = "directory"
    else:
        print(f"mdr: error: {args.path} is not a file or directory", file=sys.stderr)
        sys.exit(1)

    serve(path, mode, port=args.port, open_browser=not args.no_open)
