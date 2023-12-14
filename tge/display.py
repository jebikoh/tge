import os
import sys
import numpy as np
import signal

CLEAR = "\033[2J"
HOME = "\033[H"
CHAR_SET = [" ", ".", ",", "-", "~", ":", ";", "=", "!", "*", "#", "$", "@"]


def get_terminal_size():
    """Get the size of the terminal

    Returns:
        (int, int): width and height of the terminal
    """
    height, width = os.popen("stty size", "r").read().split()
    return int(width), int(height)


def clear():
    """Clear the terminal"""
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
            width (int, optional): Width of display. Defaults to 25.
            height (int, optional): Height of display. Defaults to 25.
            hspace (int, optional): Space between dispaly rows. Defaults to 2.
        """
        self.width = width
        self.height = height
        self.hspace = hspace
        self.buf = np.full((height, width), "@", dtype="<U1")
        self.start_row, self.start_col = self._calculate_start_pos()
        self.debug_buf = None
        signal.signal(signal.SIGWINCH, self._handle_resize)

    def _calculate_start_pos(self):
        w, h = get_terminal_size()
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

    def update_buffer(self, r: np.ndarray, debug=False):
        """Converts render output to a character-based buffer and updates frame buffer

        Args:
            new_buf (np.ndarray): Render output
            debug (bool): Whether to save the render output to the debug buffer

        Raises:
            ValueError: If the shape of new_buf does not match the shape of the current buffer
        """
        if r.shape != self.buf.shape:
            raise ValueError(
                f"Render output shape {r.shape} does not match buffer shape {self.buf.shape}"
            )
        if debug:
            self.debug_buf = r
        r_i = np.round(r * (len(CHAR_SET) - 1)).astype(int)
        self.buf = np.array(CHAR_SET)[r_i]

    def render_buffer(self):
        """Render the buffer to the terminal"""
        fbuf = self._buf_to_fb()
        _write(fbuf)
        _flush()
