"""Entry point for the news-image-20261121 submission.

The platform runs this with the output directory as argv[1] and then reads
entry.png from inside that directory. So argv[1] is a directory, never a file
path: treating it as a filename is the single easiest way to fail the check.

The image itself is built by render.py, which writes entry.png next to this
file. This script only has to put those exact bytes where the platform looks,
so it copies rather than re-renders: a re-render could differ by a pixel and
make the submitted artifact something nobody verified.

Standard library only. No network. No third-party packages.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "entry.png"


def source_image():
    """The verified image that sits beside this script."""
    path = os.path.join(HERE, IMAGE_NAME)
    if not os.path.isfile(path):
        raise SystemExit(
            "missing %s next to main.py - run `python3 render.py entry.png` first"
            % IMAGE_NAME)
    return path


def target_dir(argv):
    """Resolve the output directory from argv, then env, then ./output."""
    if len(argv) > 1 and argv[1].strip():
        return argv[1]
    from_env = os.environ.get("OUTPUT_DIR", "").strip()
    if from_env:
        return from_env
    return os.path.join(os.getcwd(), "output")


def main(argv):
    out_dir = target_dir(argv)
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, IMAGE_NAME)
    shutil.copyfile(source_image(), destination)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
