#!/usr/bin/env python3
"""news-image-20261124 entrypoint.

Copies the pre-rendered front page (entry.png, shipped in this repository)
to the grader's output directory. No network, no randomness, no clock:
every run writes the same bytes, so the two grader runs are identical.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET_NAME = "entry.png"


def resolve_output_dir():
    """The grader runs with a writable /output; honour an explicit
    MAKEFUN_OUTPUT_DIR first so local runs can point elsewhere."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return wanted


def main():
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, TARGET_NAME)
    shutil.copyfile(SOURCE, target)
    # Verify the copy is a whole PNG before reporting success: the first
    # eight bytes of any PNG are a fixed signature, so a truncated or
    # corrupted write is caught here instead of silently passing.
    with open(target, "rb") as handle:
        magic = handle.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("refusing to report success: %s is not a PNG" % target)
    print("wrote %s (%d bytes)" % (target, os.path.getsize(target)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
