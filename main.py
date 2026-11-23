#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The grader runs this with a read-only repository, so nothing is ever
written next to this file: the destination is always inside
MAKEFUN_OUTPUT_DIR (default "out" for local runs).
"""
import hashlib
import os
import shutil
import struct
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("FAIL: output is not a PNG", file=sys.stderr)
        return 1
    if len(data) > 1048576:
        print(f"FAIL: output {len(data)} bytes exceeds 1 MiB", file=sys.stderr)
        return 1
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (1024, 1024):
        print(f"FAIL: expected 1024x1024, got {w}x{h}", file=sys.stderr)
        return 1
    with open(src, "rb") as f:
        src_data = f.read()
    if hashlib.sha256(data).hexdigest() != hashlib.sha256(src_data).hexdigest():
        print("FAIL: sha256 mismatch", file=sys.stderr)
        return 1
    print(f"OK: wrote {dst} ({len(data)} bytes, 1024x1024)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
