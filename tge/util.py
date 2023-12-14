import numpy as np
from enum import Enum


def normalize(v: np.ndarray) -> np.ndarray:
    """Normalize a vector

    Args:
        v (np.ndarray): Vector to normalize

    Returns:
        (np.ndarray): Normalized vector
    """
    return v / np.linalg.norm(v)


class Vec3:
    """Represents a 3D vector"""

    def __init__(self, x: float, y: float, z: float):
        """Initialize a 3D vector

        Args:
            x (float): x component
            y (float): y component
            z (float): z component
        """
        self.v = np.array([x, y, z])

    def __add__(self, other) -> "Vec3":
        """Add two vectors

        Args:
            other (Vec3 | np.ndarray): Other vector to add. Must be Vec3 or np.ndarray of shape (3,)

        Raises:
            ValueError: If other is np.ndarray of wrong shape
            TypeError: If other is not Vec3 or np.ndarray

        Returns:
            (Vec3): Sum of vectors
        """
        if isinstance(other, Vec3):
            v = self.v + other.v
            return Vec3(v[0], v[1], v[2])
        elif isinstance(other, np.ndarray):
            if other.shape != (3,):
                raise ValueError("Vector must be 3 dimensional")
            v = self.v + other
            return Vec3(v[0], v[1], v[2])
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other) -> "Vec3":
        """Subtract two vectors

        Args:
            other (Vec3 | np.ndarray): Other vector to subtract. Must be Vec3 or np.ndarray of shape (3,)

        Raises:
            ValueError: If other is np.ndarray of wrong shape
            TypeError: If other is not Vec3 or np.ndarray

        Returns:
            (Vec3): Difference of vectors
        """
        if isinstance(other, Vec3):
            v = self.v - other.v
            return Vec3(v[0], v[1], v[2])
        elif isinstance(other, np.ndarray):
            if other.shape != (3,):
                raise ValueError("Vector must be 3 dimensional")
            v = self.v - other
            return Vec3(v[0], v[1], v[2])
        else:
            raise TypeError("Unsupported operand type for -")

    def normalize(self):
        """Normalize vector

        Returns:
            (Vec3): Returns self (normalized)
        """
        self.v = normalize(self.v)
        return self


class Vec4:
    """Represents a 3D vector with a homogeneous coordinate"""

    def __init__(self, x: float, y: float, z: float, w: float):
        """Initialize a 3D vector with a homogeneous coordinate

        Args:
            x (float): x component
            y (float): y component
            z (float): z component
            w (float): w component
        """
        self.v = np.array([x, y, z, w])


# Transformations
class Axis(Enum):
    """Enum for axis"""

    X = 0
    Y = 1
    Z = 2


def build_rotation(rad: float, axis: Axis) -> np.ndarray:
    """Builds a rotation matrix along the given axis by given radians

    Args:
        rad (float): Rotation in radians
        axis (Axis): Axis of rotation

    Returns:
        (np.ndarray): Rotation matrix (4x4)
    """
    if axis == Axis.X:
        c, s = np.cos(rad), np.sin(rad)
        return np.array(
            [
                [1, 0, 0, 0],
                [0, c, -s, 0],
                [0, s, c, 0],
                [0, 0, 0, 1],
            ]
        )
    if axis == Axis.Y:
        c, s = np.cos(rad), np.sin(rad)
        return np.array(
            [
                [c, 0, s, 0],
                [0, 1, 0, 0],
                [-s, 0, c, 0],
                [0, 0, 0, 1],
            ]
        )
    else:
        c, s = np.cos(rad), np.sin(rad)
        return np.array(
            [
                [c, -s, 0, 0],
                [s, c, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )


def build_rotation_deg(deg: float, axis: Axis) -> np.ndarray:
    """Builds a rotation matrix along the given axis by given degrees. Wrapper for rotation_matrix().

    Args:
        deg (float): Rotation in degrees
        axis (Axis): Axis of rotation

    Returns:
        (np.ndarray): Rotation matrix (4x4)
    """
    return build_rotation(np.deg2rad(deg), axis)


def build_translation(t_x: float, t_y: float, t_z: float) -> np.ndarray:
    """Builds a translation matrix by given x, y, and z translations

    Args:
        t_x (float): Translation in x
        t_y (float): Translation in y
        t_z (float): Translation in z

    Returns:
        (np.ndarray): Translation matrix (4x4)
    """
    return np.array(
        [
            [1, 0, 0, t_x],
            [0, 1, 0, t_y],
            [0, 0, 1, t_z],
            [0, 0, 0, 1],
        ]
    )


def build_scale(s_x: float, s_y: float, s_z: float) -> np.ndarray:
    """Builds a scale matrix by given x, y, and z scales

    Args:
        s_x (float): Scale in x
        s_y (float): Scale in y
        s_z (float): Scale in z

    Returns:
        (np.ndarray): Scale matrix (4x4)
    """
    return np.array(
        [
            [s_x, 0, 0, 0],
            [0, s_y, 0, 0],
            [0, 0, s_z, 0],
            [0, 0, 0, 1],
        ]
    )


def condense_transformations(transforms: list[np.ndarray]) -> np.ndarray:
    """Condenses a list of transformations into a single transformation matrix.

    Note, this method is not particularly efficient for large lists of transformations.

    Args:
        transforms (list[np.ndarray]): Transformations in order (from left to right)

    Returns:
        (np.ndarray): Condensed transformation matrix (4x4)
    """
    result = np.eye(4)
    for T in transforms:
        result = result @ T

    return result
