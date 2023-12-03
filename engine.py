import numpy as np
from display import Display
from model import Model
from scene import Camera


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

    def remove_model(self, id: int):
        self.models.pop(id)

    def transform_model(self, m_id: int, t: np.ndarray):
        if t.shape != (4, 4):
            raise ValueError("Transformation matrix must be 4x4")
        self.models[m_id].apply_transform(t)

    def add_camera(self, camera: Camera):
        self.camera.append(camera)
        return len(self.camera) - 1

    def remove_camera(self, id: int):
        self.camera.pop(id)

    def render(self):
        pass

    def _apply_view_transform(self, camera_id: int):
        """Apply the view transform to all models

        Args:
            camera_id (int): ID of the camera to use

        Returns:
            List[np.ndarray]: List of transformed models
        """
        out = []
        for model in self.models:
            out.append(model.apply_transform(self.camera[camera_id].get_view_matrix()))
        return out
