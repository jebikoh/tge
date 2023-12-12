import numpy as np
from .util import Vec3


class DirectionalLight:
    """Class representing a directional light source."""

    def __init__(self, direction: Vec3):
        """Create a directional light source

        Args:
            direction (Vec3): Direction of the light source (direction the light is going towards)
        """
        self.dir = direction.normalize()

    def compute_intensity(self, surface_normal: Vec3 | np.ndarray) -> float:
        """Computes the intensity of the light source on a surface

        Args:
            surface_normal (Vec3 | np.ndarray): Surface normal of a face

        Raises:
            ValueError: If surface normal is provided as np.ndarrray and is not 3x1

        Returns:
            float: Intensity of the light source on the surface [0, 1]
        """
        if isinstance(surface_normal, Vec3):
            return max(0, -np.dot(surface_normal.v, self.dir.v))
        else:
            if surface_normal.shape != (3,):
                raise ValueError("Surface normal must be 3x1")
            return max(0, -np.dot(surface_normal, self.dir.v))


class PointLight:
    def __init__(self, position: Vec3):
        self.pos = position


class SpotLight:
    def __init__(self, position: Vec3, direction: Vec3, angle: float):
        self.pos = position
        self.dir = direction
        self.angle = angle
