import os
import sys
import numpy as np
import signal

CLEAR = "\033[2J"
HOME = "\033[H"
CHAR_SET = [".", ",", "-", "~", ":", ";", "=", "!", "*", "#", "$", "@"]


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
    """Display class for rendering a character-based buffer to the terminal"""

    def __init__(self, width: int = 25, height: int = 25, hspace: int = 2):
        """Initialize the display

        Args:
            width (int, optional): width of display. Defaults to 25.
            height (int, optional): height of display. Defaults to 25.
            hspace (int, optional): space between dispaly rows. Defaults to 2.
        """
        self.width = width
        self.height = height
        self.hspace = hspace
        self.buf = np.full((height, width), "@", dtype="<U1")
        self.start_row, self.start_col = self._calculate_start_pos()
        signal.signal(signal.SIGWINCH, self._handle_resize)

    def _calculate_start_pos(self):
        w, h = _get_terminal_size()
        start_row = max((h - self.height) // 2, 0)
        start_column = max((w - self.width * self.hspace) // 2, 0)
        return start_row, start_column

    def _buf_to_fb(self):
        spaces = ["".join(char * self.hspace for char in line) for line in self.buf]
        fbuf = [
            f"\033[{self.start_row + i};{self.start_col}H{line}"
            for i, line in enumerate(spaces)
        ]
        return CLEAR + "\n".join(fbuf)

    def _handle_resize(self, signum, frame):
        self.start_row, self.start_col = self._calculate_start_pos()

    def build_empty_buffer(self):
        """Build an empty buffer"""
        return np.full((self.height, self.width), " ", dtype="<U1")

    def update_buffer(self, new_buf: np.ndarray):
        """Update the buffer with new content

        Args:
            new_buf (np.ndarray): new buffer

        Raises:
            ValueError: if the shape of new_buf does not match the shape of the current buffer
        """
        if new_buf.shape != self.buf.shape:
            raise ValueError(
                f"New content shape {new_buf.shape} does not match buffer shape {self.buf.shape}"
            )
        # Add logic here to update self.buf with new_content
        self.buf = new_buf

    def render(self):
        """Render the buffer to the terminal"""
        fbuf = self._buf_to_fb()
        _write(fbuf)
        _flush()
