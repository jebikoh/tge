import re
import numpy as np
from enum import Enum


def normalize(v: np.ndarray):
    """Normalize a vector

    Args:
        v (np.ndarray): Vector to normalize

    Returns:
        np.ndarray: Normalized vector
    """
    return v / np.linalg.norm(v)


class Vec3:
    def __init__(self, x: float, y: float, z: float):
        self.v = np.array([x, y, z])

    def __add__(self, other):
        v = self.v + other.v
        return Vec3(v[0], v[1], v[2])

    def __sub__(self, other):
        v = self.v - other.v
        return Vec3(v[0], v[1], v[2])

    def normalize(self):
        """Normalize the vector"""
        self.v = normalize(self.v)
        return self


class Vec4:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.v = np.array([x, y, z, w])


# Transformations
class Axis(Enum):
    X = 0
    Y = 1
    Z = 2


def build_rotation(rad: float, axis: Axis):
    """Builds a rotation matrix along the given axis by given radians

    Args:
        rad (float): Rotation in radians
        axis (Axis): Axis of rotation

    Returns:
        _type_: Rotation matrix (4x4)
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


def build_rotation_deg(deg: float, axis: Axis):
    """Builds a rotation matrix along the given axis by given degrees. Wrapper for rotation_matrix().

    Args:
        deg (float): Rotation in degrees
        axis (Axis): Axis of rotation

    Returns:
        _type_: Rotation matrix (4x4)
    """
    return build_rotation(np.deg2rad(deg), axis)


def build_translation(t_x: float, t_y: float, t_z: float):
    """Builds a translation matrix by given x, y, and z translations

    Args:
        t_x (float): Translation in x
        t_y (float): Translation in y
        t_z (float): Translation in z

    Returns:
        _type_: Translation matrix (4x4)
    """
    return np.array(
        [
            [1, 0, 0, t_x],
            [0, 1, 0, t_y],
            [0, 0, 1, t_z],
            [0, 0, 0, 1],
        ]
    )


def build_scale(s_x: float, s_y: float, s_z: float):
    """Builds a scale matrix by given x, y, and z scales

    Args:
        s_x (float): Scale in x
        s_y (float): Scale in y
        s_z (float): Scale in z

    Returns:
        _type_: Scale matrix (4x4)
    """
    return np.array(
        [
            [s_x, 0, 0, 0],
            [0, s_y, 0, 0],
            [0, 0, s_z, 0],
            [0, 0, 0, 1],
        ]
    )


def condense_transformations(transforms: list[np.ndarray]):
    """Condenses a list of transformations into a single transformation matrix.

    Note, this method is not particularly efficient for large lists of transformations.

    Args:
        transforms (list[np.ndarray]): Transformations in order (from left to right)
    """
    result = np.eye(4)
    for T in transforms:
        result = result @ T

    return result
