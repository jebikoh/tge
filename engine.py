import numpy as np
from display import Display
from model import Model


class GraphicsEngine:
    def __init__(self, resolution: tuple[int, int], ups: int = 60):
        """Graphics engine that can render, shade, and manipulate 3D models

        Args:
            resolution (tuple[int, int]): Resolution of the display (width, height) in characters
            ups (int, optional): Display updates per second. Defaults to 60.
        """
        self.display = Display(resolution[0], resolution[1])
        self.ups = ups
        self.models = []
        self.lights = []
        self.camera = []

    def add_model(self, model: Model):
        self.models.append(model)
        return len(self.models) - 1

    def remove_model(self, index: int):
        self.models.pop(index)

    def transform_model(self, m_id: int, t: np.ndarray):
        if t.shape != (4, 4):
            raise ValueError("Transformation matrix must be 4x4")
        self.models[m_id].apply_transform(t)
