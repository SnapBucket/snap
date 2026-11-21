#!/usr/bin/env python3
"""Entry program for the make.fun news-image contest.

The platform runs this with the output directory as argv[1] and reads
<dir>/entry.png. The picture is pre-rendered and committed next to this file,
so this program needs no network and no third-party packages: it copies bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
NAME = "entry.png"


def target_dir(argv):
    """argv[1] is a DIRECTORY, not a file path. Fall back to env, then ./output."""
    if len(argv) > 1 and argv[1].strip():
        return argv[1]
    env = os.environ.get("OUTPUT_DIR")
    if env and env.strip():
        return env
    return os.path.join(os.getcwd(), "output")


def main(argv):
    out = target_dir(argv)
    os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, NAME)
    if not os.path.isfile(SOURCE):
        sys.stderr.write("missing pre-rendered image: %s\n" % SOURCE)
        return 1
    shutil.copyfile(SOURCE, dest)
    if os.path.getsize(dest) != os.path.getsize(SOURCE):
        sys.stderr.write("short copy: %s\n" % dest)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
