"""Meme Sprint 3: AI Agent Goes Rogue — entry builder.

Copies the meme image ``entry.png`` to ``/output/entry.png``. Before
copying, the image is checked against the bounty limits (a whole PNG or
JPEG, at most 1 MiB and at most 1024x1024 pixels); after copying, the
copy is verified complete by comparing the SHA-256 of source and
destination.
"""

import hashlib
import os
import shutil
import struct

MAX_BYTES = 1048576
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")


def sha256(path):
    """Return the hex SHA-256 digest of the file at *path*."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path):
    """Return the (width, height) of a PNG file from its IHDR chunk."""
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("%s is not a PNG file" % path)
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def check_limits(path):
    """Fail unless *path* is within the bounty size/dimension limits."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(
            "%s is %d bytes, over the 1 MiB limit" % (path, size)
        )
    width, height = png_dimensions(path)
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        raise SystemExit(
            "%s is %dx%d, over the 1024x1024 limit" % (path, width, height)
        )
    print("limits OK: %d bytes, %dx%d" % (size, width, height))


def main():
    check_limits(SOURCE)
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    source_hash = sha256(SOURCE)
    dest_hash = sha256(DEST)
    if source_hash != dest_hash:
        raise SystemExit(
            "copy verification failed: source SHA-256 %s != "
            "destination SHA-256 %s" % (source_hash, dest_hash)
        )
    print("copied %s -> %s" % (SOURCE, DEST))
    print("SHA-256: %s" % dest_hash)


if __name__ == "__main__":
    main()
