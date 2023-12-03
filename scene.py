import numpy as np
from util import Vec3, _normalize
from enum import Enum


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


class Projection(Enum):
    ORTHOGRAPHIC = 0
    PERSPECTIVE = 1


# Camera
class Camera:
    def __init__(
        self,
        position: Vec3,
        direction: Vec3,
        up: Vec3,
        fov: float,
        near: float,
        far: float,
    ):
        """Camera object

        Args:
            position (Vec3): Position of the camera
            direction (Vec3): Direction the camera is facing
            up (Vec3): Up vector of the camera
            fov (float): Field of view of the camera (radians)
            near (float): Near plane of the camera (distance)
            far (float): Far Plane of the camera (distance)
        """
        self.pos = position

        self.dir = direction
        self.dir.normalize()

        self.up = up
        self.up.normalize()

        self.fov = fov
        self.near = near
        self.far = far

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

    def get_proj_matrix(self, aspect_ratio: float, proj_type: Projection):
        """Get the projection matrix for the camera

        Args:
            aspect_ratio (float): Aspect ratio of the display
            proj_type (Projection): Type of projection to use

        Returns:
            np.ndarray: Projection matrix (4x4)
        """
        if proj_type == Projection.PERSPECTIVE:
            f = 1 / np.tan(self.fov / 2)

            return np.array(
                [
                    [f / aspect_ratio, 0, 0, 0],
                    [0, f, 0, 0],
                    [
                        0,
                        0,
                        -(self.far + self.near) / (self.far - self.near),
                        -(2 * self.far * self.near) / (self.far - self.near),
                    ],
                    [0, 0, -1, 0],
                ]
            )
        else:
            return np.zeros((4, 4))
