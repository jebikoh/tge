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

    def render(
        self,
        camera_id: int,
        proj_type: Projection = Projection.PERSPECTIVE,
        debug=False,
    ):
        """Render the scene

        Args:
            camera_id (int): ID of the camera to use for rendering
            proj_type (Projection, optional): Type of projection to use. Defaults to Projection.PERSPECTIVE.
        """
        models = []
        camera = self.camera[camera_id]
        view_matrix = camera.get_view_matrix()
        proj_matrix = camera.get_proj_matrix(self.aspect_ratio, proj_type)
        t = proj_matrix @ view_matrix
        if debug:
            print("View Matrix:")
            print(view_matrix)
            print("Projection Matrix:")
            print(proj_matrix)
            print("Transform Matrix:")
            print(t)

        for model in self.models:
            m = apply_transform(model, t)
            # Skipping clipping for now; add later if needed
            # Perspective Division
            m.v = m.v / m.v[:, 3].reshape(-1, 1)
            if debug:
                print("NDC:")
                print(m.v)
            # Convert NDC to screen (in-place)
            self._ndc_to_screen(m)
            models.append(m)
            if debug:
                print("Screen space:")
                print(m.v)

            # Back-face culling
            for i, face in enumerate(m.f):
                view = camera.pos - m.v[face[0]]
                if np.dot(m.n[i], view) > 0:
                    continue

        # Lighting
        # Depth-testing
        # Frame Buffering

    def _ndc_to_screen(self, m: Model, inv_y: bool = False):
        """Converts a model with points in NDC to screen coordinates (in-place)

        Args:
            m (Model): model to convert
        """
        screen_v = (m.v + 1) / 2
        screen_v[:, 0] *= self.display.width
        screen_v[:, 1] *= self.display.height

        if inv_y:
            screen_v[:, 1] = self.display.height - screen_v[:, 1]

        m.v = screen_v


def _is_back_face(normal: np.ndarray, view: np.ndarray) -> bool:
    return np.dot(normal, view) > 0
