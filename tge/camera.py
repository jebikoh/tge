import numpy as np
from .util import Vec3, normalize
from enum import Enum


class Projection(Enum):
    """Enum for projection types"""

    ORTHOGRAPHIC = 0
    PERSPECTIVE = 1


class Camera:
    """Represents a camera"""

    def __init__(
        self,
        position: Vec3,
        target: Vec3,
        up: Vec3,
        fov: float,
        near: float,
        far: float,
    ):
        """Initialize a camera

        Args:
            position (Vec3): Position of the camera
            target (Vec3): Position the camera is looking at
            up (Vec3): Up vector of the camera
            fov (float): Field of view of the camera (radians)
            near (float): Near plane of the camera (distance)
            far (float): Far Plane of the camera (distance)
        """
        self.pos = position

        self.dir = target - self.pos
        self.dir.normalize()

        self.up = up
        self.up.normalize()

        self.fov = fov
        self.near = near
        self.far = far

    def get_view_matrix(self) -> np.ndarray:
        """Get the view matrix for the camera

        Returns:
            (np.ndarray): View matrix (4x4)
        """
        right = normalize(np.cross(self.dir.v, self.up.v))
        up = normalize(np.cross(right, self.dir.v))

        return np.array(
            [
                [right[0], right[1], right[2], -np.dot(right, self.pos.v)],
                [up[0], up[1], up[2], -np.dot(up, self.pos.v)],
                [
                    -self.dir.v[0],
                    -self.dir.v[1],
                    -self.dir.v[2],
                    np.dot(self.dir.v, self.pos.v),
                ],
                [0, 0, 0, 1],
            ]
        )

    def get_proj_matrix(self, aspect_ratio: float, proj_type: Projection) -> np.ndarray:
        """Get the projection matrix for the camera

        Args:
            aspect_ratio (float): Aspect ratio of the display
            proj_type (Projection): Type of projection to use

        Returns:
            (np.ndarray): Projection matrix (4x4)
        """
        f = 1 / np.tan(self.fov / 2)
        if proj_type == Projection.PERSPECTIVE:
            return np.array(
                [
                    [f / aspect_ratio, 0, 0, 0],
                    [0, f, 0, 0],
                    [
                        0,
                        0,
                        (self.far + self.near) / (self.far - self.near),
                        (2 * self.far * self.near) / (self.far - self.near),
                    ],
                    [0, 0, -1, 0],
                ]
            )
        else:
            return np.zeros((4, 4))
