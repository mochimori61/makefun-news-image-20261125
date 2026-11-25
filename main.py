#!/usr/bin/env python3
"""THE MIDNIGHT GAZETTE — entrypoint (Akun 20, News Image 20261125).

entry.png, resting beside this file, is the finished page.
This entrypoint feeds it to /output/entry.png through a
block generator and shutil.copyfileobj — the bytes arrive
exactly as printed. Standard library only.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET_DIR = "/output"
TARGET = os.path.join(TARGET_DIR, "entry.png")
BLOCK = 16384


def blocks(stream):
    while True:
        chunk = stream.read(BLOCK)
        if not chunk:
            return
        yield chunk


def deliver() -> int:
    os.makedirs(TARGET_DIR, exist_ok=True)
    written = [0]

    class Tally:
        def write(self, data):
            written[0] += len(data)
            return len(data)

        def flush(self):
            pass

    with open(SOURCE, "rb") as src, open(TARGET, "wb") as dst:
        shutil.copyfileobj(_Feed(blocks(src)), _Join(dst, Tally()))
    return written[0]


class _Feed:
    def __init__(self, gen):
        self._gen = gen
        self._buf = b""

    def read(self, n=-1):
        if n is None or n < 0:
            return b"".join([self._buf, *self._gen])
        while len(self._buf) < n:
            try:
                self._buf += next(self._gen)
            except StopIteration:
                break
        out, self._buf = self._buf[:n], self._buf[n:]
        return out


class _Join:
    def __init__(self, dst, tally):
        self._dst = dst
        self._tally = tally

    def write(self, data):
        self._tally.write(data)
        return self._dst.write(data)

    def flush(self):
        self._dst.flush()


if __name__ == "__main__":
    print(f"delivered {deliver()} bytes to {TARGET}")
