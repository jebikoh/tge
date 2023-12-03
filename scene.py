import numpy as np
from util import Vec3, _normalize


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


# Camera
class Camera:
    def __init__(self, position: Vec3, direction: Vec3, up: Vec3, fov: float):
        self.pos = position

        self.dir = direction
        self.dir.normalize()

        self.up = up
        self.up.normalize()

        self.fov = fov

    def get_view_matrix(self):
        """Get the view matrix for the camera

        Returns:
            np.ndarray: View matrix (4x4)
        """
        right = _normalize(np.cross(self.up.v, self.dir.v))
        adj_up = np.cross(right, self.dir.v)

        return np.array(
            [
                [right[0], right[1], right[2], -np.dot(right, self.pos.v)],
                [adj_up[0], adj_up[1], adj_up[2], -np.dot(adj_up, self.pos.v)],
                [
                    self.dir.v[0],
                    self.dir.v[1],
                    self.dir.v[2],
                    -np.dot(self.dir.v, self.pos.v),
                ],
                [0, 0, 0, 1],
            ]
        )
