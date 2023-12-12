import numpy as np
from .util import Vec3


class DirectionalLight:
    def __init__(self, direction: Vec3):
        self.dir = direction.normalize()

    def compute_intensity(self, surface_normal: Vec3) -> float:
        return max(0, np.dot(surface_normal.v, self.dir.v))


class PointLight:
    def __init__(self, position: Vec3):
        self.pos = position


class SpotLight:
    def __init__(self, position: Vec3, direction: Vec3, angle: float):
        self.pos = position
        self.dir = direction
        self.angle = angle
