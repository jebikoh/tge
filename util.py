import numpy as np


class Vec3:
    def __init__(self, x: float, y: float, z: float):
        self.v = np.array([x, y, z])


class Vec4:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.v = np.array([x, y, z, w])
