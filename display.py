import os
import sys
import numpy as np
import signal

CLEAR = "\033[2J"
HOME = "\033[H"
CHAR_SET = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]


def _get_terminal_size():
    height, width = os.popen("stty size", "r").read().split()
    return int(width), int(height)


def clear():
    _write(f"{CLEAR}{HOME}")
    _flush()


def _flush():
    sys.stdout.flush()


def _write(m: str):
    sys.stdout.write(m)


class Display:
    def __init__(self, width: int = 25, height: int = 25):
        self.width = width
        self.height = height
        self.buf = np.full((height, width), "@", dtype="<U1")
        self.start_row, self.start_col = self._calculate_start_pos()
        signal.signal(signal.SIGWINCH, self._handle_resize)

    def _calculate_start_pos(self):
        w, h = _get_terminal_size()
        start_row = max((h - self.height) // 2, 0)
        start_column = max((w - self.width) // 2, 0)
        return start_row, start_column

    def _buf_to_fb(self):
        return CLEAR + "\n".join(
            [
                f"\033[{self.start_row + i};{self.start_col}H{''.join(line)}"
                for i, line in enumerate(self.buf)
            ]
        )

    def _handle_resize(self, signum, frame):
        self.start_row, self.start_col = self._calculate_start_pos()

    def update_buffer(self, new_content):
        # Add logic here to update self.buf with new_content
        pass

    def render(self):
        fbuf = self._buf_to_fb()
        _write(fbuf)
        _flush()
