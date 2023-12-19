import ctypes
import os

lib_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "c_lib", "build", "add.so")
)
c_lib = ctypes.CDLL(lib_path)

c_lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
c_lib.add.restype = ctypes.c_int


def add_nums(a, b):
    result = c_lib.add(a, b)
    return result


if __name__ == "__main__":
    print(add_nums(1, 2))
