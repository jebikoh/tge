import numpy as np
from .util import normalize


class Model:
    """Class representing a 3D model. Defined by vertices and faces. Uses left-handed coordinate system."""

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

    def compute_normals(self) -> np.ndarray:
        """Compute normals for each face

        Returns:
            (np.ndarray): matrix of normals for each face. Shape (n, 3) where n is the number of faces
        """
        norms = []
        for face in self.f:
            v0, v1, v2 = (self.v[:, :-1])[face]
            norms.append(normalize(np.cross(v1 - v0, v2 - v0)))
        return np.array(norms)

    def round_vertices(self):
        """Round vertices to nearest integer"""
        self.v = np.rint(self.v).astype(int)


def apply_transform(model: Model, t: np.ndarray) -> Model:
    """Apply a transformation to a model

    Args:
        model (Model): Model to transform
        t (np.ndarray): 4x4 transformation matrix

    Raises:
        ValueError: If transformation matrix is not 4x4

    Returns:
       (Model): Transformed model
    """
    if t.shape != (4, 4):
        raise ValueError("Transformation matrix must be 4x4")

    return Model(model.v @ t.T, model.f.copy())


def load_model(path: str) -> Model:
    """Load a model from a .obj file. At the moment, this only supports vertices and faces.

    Args:
        path (str): Path to .obj file

    Returns:
        (Model): object from .obj file
    """
    vertices = []
    faces = []

    with open(path, "r") as f:
        for line in f:
            if line.startswith("v "):
                v = [float(num) for num in line[2:].strip().split(" ") if num] + [1.0]
                # TGE is left-handed, so we need to flip this coordinate
                v[2] *= -1
                vertices.append(v)

            elif line.startswith("f "):
                faces.append(
                    [
                        (int(face.split("/")[0]) - 1)
                        for face in line[2:].strip().split(" ")
                        if face
                    ]
                )
            else:
                continue

    return Model(np.array(vertices), np.array(faces))
