import numpy as np
from .display import Display
from .model import Model, apply_transform
from .scene import Camera, Projection
from .util import Vec3
from .debug import plot_scatter, plot_scene

ORIGIN = Vec3(0, 0, 0)


class GraphicsEngine:
    """Graphics engine for rendering 3D models to the terminal. Handles rendering pipeline and rasterization."""

    def __init__(self, resolution: tuple[int, int], ups: int = 60):
        """Initialize a graphics engine

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

    def add_model(self, model: Model) -> int:
        """Add a model to the scene

        Args:
            model (Model): Model to add

        Returns:
            (int): model ID
        """
        self.models.append(model)
        return len(self.models) - 1

    def remove_model(self, id: int):
        """Removes a model from the scene

        Args:
            id (int): model ID
        """
        self.models.pop(id)

    def transform_model(self, m_id: int, t: np.ndarray):
        """Apply a transformation to a model in the scene

        Args:
            m_id (int): model ID
            t (np.ndarray): transformation matrix to apply (4x4)

        Raises:
            ValueError: If transformation matrix is not 4x4
            IndexError: If model ID is invalid
        """
        if t.shape != (4, 4):
            raise ValueError("Transformation matrix must be 4x4")
        if m_id >= len(self.models):
            raise IndexError("Model ID out of range")
        self.models[m_id].apply_transform(t)

    def add_camera(self, camera: Camera) -> int:
        """Add a camera to the scene

        Args:
            camera (Camera): Camera to add

        Returns:
            (int): camera ID
        """
        self.camera.append(camera)
        return len(self.camera) - 1

    def remove_camera(self, id: int):
        """Removes a camera from the scene

        Args:
            id (int): camera ID

        Raises:
            IndexError: if camera ID is invalid
        """
        if id >= len(self.camera):
            raise IndexError("Camera ID out of range")
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
        buf = self.display.build_empty_buffer()
        camera = self.camera[camera_id]
        view_matrix = camera.get_view_matrix()
        proj_matrix = camera.get_proj_matrix(self.aspect_ratio, proj_type)
        t = proj_matrix @ view_matrix
        if debug:
            print("View Matrix:\n" + str(view_matrix))
            print("Projection Matrix:\n" + str(proj_matrix))
            print("Transform Matrix:\n" + str(t))

        for model in self.models:
            m = apply_transform(model, t)
            if debug:
                # Origin model
                print("Origin model:\n" + str(model.v))
                plot_scene(model, camera.pos, title="Origin scene")
                print("Transformed model:\n" + str(m.v))
                plot_scene(m, ORIGIN, title="Transformed scene")

            # Skipping clipping for now; add later if needed
            # Perspective Division
            m.v = m.v / m.v[:, 3].reshape(-1, 1)
            if debug:
                print("NDC:\n" + str(m.v))
                plot_scene(m, ORIGIN, title="NDC")

            # Convert NDC to screen (in-place)
            self._ndc_to_screen(m)
            m.round_vertices()

            if debug:
                print("Screen space:\n" + str(m.v))
            # Rasterization
            norms = m.compute_normals()
            for i, face in enumerate(m.f):
                view = camera.pos.v - (m.v[face[0]])[:-1]
                # Back-face culling
                # if np.dot(norms[i], view) > 0:
                #     if debug:
                #         print(f"Culled face {i}")
                #     continue
                v0, v1, v2 = m.v[face]
                _bresenhams_line(v0[0], v1[0], v0[1], v1[1], buf)
                _bresenhams_line(v1[0], v2[0], v1[1], v2[1], buf)
                _bresenhams_line(v2[0], v0[0], v2[1], v0[1], buf)
                if debug:
                    self.display.update_buffer(buf)
                    self.display.render()

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


def _bresenhams_line(x0: int, x1: int, y0: int, y1: int, buf: np.ndarray):
    h, w = buf.shape

    points = []
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1

    e = dx + dy

    points = []
    while True:
        if 0 <= x0 < w and 0 <= y0 < h:
            buf[y0, x0] = "@"
        points.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * e
        if e2 >= dy:
            e += dy
            x0 += sx
        if e2 <= dx:
            e += dx
            y0 += sy

    # print(points)
