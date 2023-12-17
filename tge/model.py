import numpy as np
from .util import normalize


class Model:
    """Class representing a 3D model. Defined by vertices and faces. Uses right-handed coordinate system."""

    def __init__(
        self, vertices: np.ndarray, faces: np.ndarray, compute_norms: bool = True
    ):
        self.v = vertices
        self.f = faces
        if compute_norms:
            self.n = self.compute_normals()
        else:
            self.n = None

    def apply_transform(self, transformation: np.ndarray, preserve_norms: bool = False):
        """Apply a transformation to the model

        Args:
            transformation (np.ndarray): 4x4 transformation matrix
            preserve_norms (bool, optional): Whether to preserve the normals of the model. Defaults to False.

        Raises:
            ValueError: If transformation matrix is not 4x4
        """
        if transformation.shape != (4, 4):
            raise ValueError("Transformation matrix must be 4x4")

        self.v = self.v @ transformation.T
        if not preserve_norms:
            self.n = self.compute_normals()

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
            (np.ndarray): Matrix of normals for each face. Shape (n, 3) where n is the number of faces
        """
        v0 = self.v[self.f[:, 0]][:, :-1]
        v1 = self.v[self.f[:, 1]][:, :-1]
        v2 = self.v[self.f[:, 2]][:, :-1]

        e1, e2 = v1 - v0, v2 - v0
        normals = np.cross(e1, e2).astype(np.float64)
        normals /= np.linalg.norm(normals, axis=1, keepdims=True)

        return normals

    def round_xy(self) -> np.ndarray:
        """Round the x and y coordinates of the vertices to the nearest integer

        Returns:
            np.ndarray: Rounded vertices
        """
        return np.rint(self.v[:, :2]).astype(int)

    def get_z(self):
        """Get z coordinates"""
        return self.v[:, 2]


def apply_transform(model: Model, t: np.ndarray, compute_norms: bool = True) -> Model:
    """Apply a transformation to a model

    Args:
        model (Model): Model to transform
        t (np.ndarray): 4x4 transformation matrix
        compute_norms (bool, optional): Whether to compute normals for the transformed model. Defaults to True.

    Raises:
        ValueError: If transformation matrix is not 4x4

    Returns:
       (Model): Transformed model
    """
    if t.shape != (4, 4):
        raise ValueError("Transformation matrix must be 4x4")

    return Model(model.v @ t.T, model.f.copy(), compute_norms=compute_norms)


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
