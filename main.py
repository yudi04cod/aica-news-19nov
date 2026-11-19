"""Entry point for the news-image-20261119 competition.

The front page image (entry.png) is drawn by draw.py with PIL and ships
in this repository. This program only copies it to the output directory
as entry.png, so it needs nothing but the Python standard library, uses
no network, and writes byte-identical output on every run.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        raise FileNotFoundError("entry.png is missing next to main.py")

    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(65536)
            if not chunk:
                break
            fout.write(chunk)


if __name__ == "__main__":
    main()
