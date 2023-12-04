from typing import List
import numpy as np
from display import Display
from model import Model, apply_transform
from scene import Camera, Projection


class GraphicsEngine:
    def __init__(self, resolution: tuple[int, int], ups: int = 60):
        """Graphics engine that can render, shade, and manipulate 3D models

        Args:
            resolution (tuple[int, int]): Resolution of the display (width, height) in characters
            ups (int, optional): Display updates per second. Defaults to 60.
        """
        self.display = Display(resolution[0], resolution[1])
        self.aspect_ratio = resolution[0] / resolution[1]
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

    def render(self, camera_id: int, proj_type: Projection = Projection.PERSPECTIVE):
        """Render the scene

        Args:
            camera_id (int): ID of the camera to use for rendering
            proj_type (Projection, optional): Type of projection to use. Defaults to Projection.PERSPECTIVE.
        """
        clip = []
        camera = self.camera[camera_id]
        view_matrix = camera.get_view_matrix()
        proj_matrix = camera.get_proj_matrix(self.aspect_ratio, proj_type)
        t = proj_matrix @ view_matrix

        for model in self.models:
            m = apply_transform(model, t)
            m.v = m.v / m.v[:, 3]
            clip.append(m)
