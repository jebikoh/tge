from typing import List, Tuple
from collections import defaultdict
import numpy as np
from .display import Display
from .model import Model, apply_transform
from .camera import Camera, Projection
from .lights import DirectionalLight, PointLight, SpotLight
from .util import Vec3
from .debug import plot_scene, pixel_map

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
        self.directional_lights = []
        self.point_lights = []
        self.spot_lights = []
        self.camera = []

    def add_model(self, model: Model) -> int:
        """Add a model to the scene

        Args:
            model (Model): Model to add

        Returns:
            (int): Model ID
        """
        self.models.append(model)
        return len(self.models) - 1

    def remove_model(self, id: int):
        """Removes a model from the scene

        Args:
            id (int): Model ID
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
            (int): Camera ID
        """
        self.camera.append(camera)
        return len(self.camera) - 1

    def remove_camera(self, id: int):
        """Removes a camera from the scene

        Args:
            id (int): Camera ID

        Raises:
            IndexError: If camera ID is invalid
        """
        if id >= len(self.camera):
            raise IndexError("Camera ID out of range")
        self.camera.pop(id)

    def add_light(self, light: DirectionalLight | PointLight | SpotLight) -> str:
        """Add a light to the scene

        Args:
            light (DirectionalLight | PointLight | SpotLight): Light to add

        Returns:
            (int): Light ID
        """
        if isinstance(light, DirectionalLight):
            self.directional_lights.append(light)
            return "d_" + str(len(self.directional_lights) - 1)
        elif isinstance(light, PointLight):
            self.point_lights.append(light)
            return "p_" + str(len(self.point_lights) - 1)
        elif isinstance(light, SpotLight):
            self.spot_lights.append(light)
            return "s_" + str(len(self.spot_lights) - 1)
        else:
            raise ValueError("Invalid light type")

    def remove_light(self, id: str):
        """Removes a light from the scene

        Args:
            id (str): Light ID

        Raises:
            IndexError: If light ID is invalid
        """
        if id.startswith("d_"):
            idx = int(id[2:])
            if idx >= len(self.directional_lights):
                raise IndexError("Light ID out of range")
            self.directional_lights.pop(idx)
        elif id.startswith("p_"):
            idx = int(id[2:])
            if idx >= len(self.point_lights):
                raise IndexError("Light ID out of range")
            self.point_lights.pop(idx)
        elif id.startswith("s_"):
            idx = int(id[2:])
            if idx >= len(self.spot_lights):
                raise IndexError("Light ID out of range")
            self.spot_lights.pop(idx)
        else:
            raise ValueError("Invalid light type")

    def render(
        self,
        camera_id: int,
        proj_type: Projection = Projection.PERSPECTIVE,
        debug=False,
    ):
        """Render a frame of the scene to the buffer

        Args:
            camera_id (int): ID of the camera to use for rendering
            proj_type (Projection, optional): Type of projection to use. Defaults to Projection.PERSPECTIVE.
        """
        buf = np.zeros((self.display.height, self.display.width))
        zbuf = np.full((self.display.height, self.display.width), -np.inf)
        h, w = buf.shape
        camera = self.camera[camera_id]
        view_matrix = camera.get_view_matrix()
        proj_matrix = camera.get_proj_matrix(self.aspect_ratio, proj_type)
        t = proj_matrix @ view_matrix
        if debug:
            print("View Matrix:\n" + str(view_matrix))
            print("Projection Matrix:\n" + str(proj_matrix))
            print("Transform Matrix:\n" + str(t))

        for model in self.models:
            if debug:
                print("Original model:\n" + str(model.v))
                plot_scene(model, camera, title="Original scene")
            m = apply_transform(model, view_matrix, compute_norms=False)
            if debug:
                print("View matrix model:\n" + str(m.v))
                plot_scene(
                    m,
                    Camera(
                        ORIGIN,
                        camera.dir,
                        camera.up,
                        camera.fov,
                        camera.near,
                        camera.far,
                    ),
                    title="View Matrix",
                )
            m.apply_transform(proj_matrix)
            if debug:
                print("Projection matrix model:\n" + str(m.v))
                plot_scene(
                    m,
                    Camera(
                        ORIGIN,
                        camera.dir,
                        camera.up,
                        camera.fov,
                        camera.near,
                        camera.far,
                    ),
                    title="Projection Matrix",
                )

            # Skipping clipping for now; add later if needed
            # Perspective Division
            m.v = m.v / m.v[:, 3].reshape(-1, 1)
            if debug:
                print("NDC:\n" + str(m.v))
                plot_scene(
                    m,
                    Camera(
                        ORIGIN,
                        camera.dir,
                        camera.up,
                        camera.fov,
                        camera.near,
                        camera.far,
                    ),
                    title="Screen space",
                )

            # Convert NDC to screen (in-place)
            self._ndc_to_screen(m, inv_y=True)
            v = m.round_xy()
            z = m.get_z()

            # Rasterization
            norms = model.n
            # Ideally, this should never happen
            if model.n is None:
                norms = m.compute_normals()
            for i, face in enumerate(m.f):
                view = camera.dir.v
                # Back-face culling
                if np.dot(norms[i], view) >= 0:
                    if debug:
                        print(f"Culled face {i}")
                    continue
                v0, v1, v2 = v[face]
                z0, z1, z2 = z[face]
                # print(f"Face {i} z-val: {z0}, {z1}, {z2}")

                # Edge walking & scan conversion
                # NOTE: this part can probably be optimized more
                edge_points = []
                edge_points += _bresenhams_line(v0, v1, z0, z1, w, h)
                edge_points += _bresenhams_line(v1, v2, z1, z2, w, h)
                edge_points += _bresenhams_line(v2, v0, z2, z0, w, h)
                edge_points = list(set(edge_points))

                intensity = (
                    self.directional_lights[-1].compute_intensity(norms[i])
                    if len(self.directional_lights) > 0
                    else 1.0
                )

                _fill_span(edge_points, buf, zbuf, intensity)
                # pixel_map(buf, path=f"debug/face_{i}.png")
        self.display.update_buffer(buf, debug=True)

    def _ndc_to_screen(self, m: Model, inv_y: bool = False):
        """Converts a model with points in NDC to screen coordinates (in-place)

        Args:
            m (Model): Model to convert
        """
        screen_v = (m.v + 1) / 2
        screen_v[:, 0] *= self.display.width
        screen_v[:, 1] *= self.display.height

        if inv_y:
            screen_v[:, 1] = self.display.height - screen_v[:, 1]

        m.v = screen_v


def _bresenhams_line(
    v0: np.ndarray, v1: np.ndarray, z0: float, z1: float, w: int, h: int
) -> List[tuple]:
    """A Bresenham's line algorithm implementation

    Args:
        v0 (np.ndarray): Starting point (x, y)
        v1 (np.ndarray): Ending point (x, y)
        z0 (float): v0 z-value
        z1 (float): v1 z-value
        w (int): Width of the buffer
        h (int): Height of the buffer

    Returns:
        (List[tuple]): List of points connecting the two points
    """
    x0, y0 = v0
    x1, y1 = v1

    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1

    zs = np.linspace(z0, z1, max(dx, abs(dy)) + 1)

    e = dx + dy

    points = []
    t = 0
    while True:
        if 0 <= x0 < w and 0 <= y0 < h:
            points.append((x0, y0, zs[t]))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * e
        if e2 >= dy:
            e += dy
            x0 += sx
        if e2 <= dx:
            e += dx
            y0 += sy

        t += 1

    return points


def _fill_span(
    edge_pts: List[Tuple[int, int]],
    buf: np.ndarray,
    zbuf: np.ndarray,
    intensity: float = 1.0,
):
    """A span fill algorithm implementation

    Args:
        edge_pts (List[Tuple[int, int]]): A list of all edge points
        buf (np.ndarray): Buffer to fill
        zbuf (np.ndarray): z-buffer
        intensity (float, optional): Intensity to fill. Defaults to 1.0.
    """
    h, w = buf.shape

    scan_lines = defaultdict(list)
    for x, y, z in edge_pts:
        scan_lines[y].append((x, z))

    for y, pts in scan_lines.items():
        if len(pts) == 1:
            x, z = pts[0]
            if 0 <= x < w and 0 <= y < h and z > zbuf[y, x]:
                buf[y, x] = intensity
                zbuf[y, x] = z
        else:
            pts.sort(key=lambda x: x[0])
            x0, z0 = pts[0]
            x1, z1 = pts[-1]
            zs = np.linspace(z0, z1, x1 - x0 + 1)
            for i in range(x0, x1 + 1):
                if 0 <= i < w and 0 <= y < h and zs[i - x0] > zbuf[y, i]:
                    buf[y, i] = intensity
                    zbuf[y, i] = zs[i - x0]
