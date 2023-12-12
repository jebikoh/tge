import numpy as np
from .util import Vec3


class DirectionalLight:
    def __init__(self, direction: Vec3):
        self.dir = direction.normalize()

    def compute_intensity(self, surface_normal: Vec3 | np.ndarray) -> float:
        if isinstance(surface_normal, Vec3):
            return max(0, np.dot(surface_normal.v, self.dir.v))
        else:
            if surface_normal.shape != (3,):
                raise ValueError("Surface normal must be 3x1")
            return max(0, np.dot(surface_normal, self.dir.v))


class PointLight:
    def __init__(self, position: Vec3):
        self.pos = position


class SpotLight:
    def __init__(self, position: Vec3, direction: Vec3, angle: float):
        self.pos = position
        self.dir = direction
        self.angle = angle
