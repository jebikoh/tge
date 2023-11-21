import numpy as np
from util import Vec3


# Light types
class DirectionalLight:
    def __init__(self, direction: Vec3):
        self.dir = direction


class PointLight:
    def __init__(self, position: Vec3):
        self.pos = position


class SpotLight:
    def __init__(self, position: Vec3, direction: Vec3, angle: float):
        self.pos = position
        self.dir = direction
        self.angle = angle
