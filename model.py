import numpy as np


class Model:
    """Class representing a 3D model. Defined by vertices and faces."""

    def __init__(self, vertices: np.ndarray, faces: np.ndarray):
        self.v = vertices
        self.f = faces

    def apply_transform(self, transformation: np.ndarray):
        """Apply a transformation to the model

        Args:
            transformation (np.ndarray): 4x4 transformation matrix

        Raises:
            ValueError: If transformation matrix is not 4x4
        """
        if transformation.shape != (4, 4):
            raise ValueError("Transformation matrix must be 4x4")

        self.v = self.v @ transformation.T

    def apply_translate(self, translation: np.ndarray):
        """Apply a translation to the model

        Args:
            translation (np.ndarray): 4x1 translation vector

        Raises:
            ValueError: If translation vector is not 4x1
        """
        if translation.shape != (4,):
            raise ValueError("Translation vector must be 4x1")
        self.v = self.v + translation


def load_model(path: str) -> Model:
    """Load a model from a .obj file

    Args:
        path (str): Path to .obj file

    Returns:
        Model: object from .obj file
    """
    vertices = []
    faces = []

    with open(path, "r") as f:
        for line in f:
            if line.startswith("v "):
                vertices.append(
                    [float(num) for num in line[2:].strip().split(" ") if num] + [1.0]
                )
            elif line.startswith("f "):
                faces.append(
                    [(int(num) - 1) for num in line[2:].strip().split(" ") if num]
                )

    return Model(np.array(vertices), np.array(faces))
