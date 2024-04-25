from typing import List
import numpy as np
from .display import Display
from .model import Model, apply_transform
from .camera import Camera, Projection
from .lights import DirectionalLight, PointLight, SpotLight
from .util import Vec3

import time

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
        self.models: List[Model] = []
        self.directional_lights: List[DirectionalLight] = []
        self.point_lights: List[PointLight] = []
        self.spot_lights: List[SpotLight] = []
        self.camera = []
        self._mlen = int(
            (resolution[0] ** 2 + resolution[1] ** 2) ** 0.5
            + resolution[0]
            + resolution[1]
        )
        self.buf = np.zeros((self.display.height, self.display.width))
        self.zbuf = np.full((self.display.height, self.display.width), -np.inf)

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

    def render(self, camera_id: int, proj_type: Projection = Projection.PERSPECTIVE):
        """Render a frame of the scene to the buffer

        Args:
            camera_id (int): ID of the camera to use for rendering
            proj_type (Projection, optional): Type of projection to use. Defaults to Projection.PERSPECTIVE.
        """
        self._clear()
        h, w = self.buf.shape
        camera = self.camera[camera_id]
        view_matrix = camera.get_view_matrix()
        proj_matrix = camera.get_proj_matrix(self.aspect_ratio, proj_type)
        t = proj_matrix @ view_matrix

        for model in self.models:
            m = apply_transform(model, t)
            # Skipping clipping for now; add later if needed
            # Perspective Division
            m.v = m.v / m.v[:, 3].reshape(-1, 1)

            # Convert NDC to screen (in-place)
            self._ndc_to_screen(m, inv_y=True)
            v = m.round_xy()
            z = m.get_z()

            ew_time = 0

            # Rasterization
            norms = model.n
            # Ideally, this should never happen
            if model.n is None:
                norms = m.compute_normals()
            for i, face in enumerate(m.f):
                view = camera.dir.v
                # Back-face culling
                if np.dot(norms[i], view) >= 0:
                    continue
                v0, v1, v2 = v[face]
                z0, z1, z2 = z[face]

                # Skip this face if all vertices are obscured
                if (
                    z0 < self.zbuf[v0[1], v0[0]]
                    and z1 < self.zbuf[v1[1], v1[0]]
                    and z2 < self.zbuf[v2[1], v2[0]]
                ):
                    continue

                # Edge walking & scan conversion
                edge_set = set()
                edge_pts = np.zeros((self._mlen, 2), dtype=int)
                edge_zs = np.zeros(self._mlen)

                j = _bresenhams_line(
                    v0, v1, z0, z1, w, h, edge_set, edge_pts, edge_zs, 0
                )
                j = _bresenhams_line(
                    v1, v2, z1, z2, w, h, edge_set, edge_pts, edge_zs, j
                )
                j = _bresenhams_line(
                    v2, v0, z2, z0, w, h, edge_set, edge_pts, edge_zs, j
                )

                edge_pts = edge_pts[0:j]
                edge_zs = edge_zs[0:j]

                intensity = 1.0
                if len(self.directional_lights) > 0:
                    intensity = 0.0
                    for light in self.directional_lights:
                        intensity += light.compute_intensity(norms[i])
                    intensity /= len(self.directional_lights)

                _fill_span(edge_pts, edge_zs, self.buf, self.zbuf, intensity)
        self.display.update_buffer(self.buf, debug=True)

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

    def _clear(self):
        self.buf.fill(0)
        self.zbuf.fill(-np.inf)


def _bresenhams_line(
    v0: np.ndarray,
    v1: np.ndarray,
    z0: float,
    z1: float,
    w: int,
    h: int,
    edge_set: set,
    edge_pts: np.ndarray,
    edge_zs: np.ndarray,
    i: int,
):
    x0, y0 = v0
    x1, y1 = v1

    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    zs = np.linspace(z0, z1, max(dx, abs(dy)) + 1)
    z_i = 0
    edge_zs[i : i + len(zs)] = zs

    e = dx + dy
    while True:
        if 0 <= x0 < w and 0 <= y0 < h and (x0, y0) not in edge_set:
            edge_set.add((x0, y0))
            edge_pts[i] = (x0, y0)
            edge_zs[i] = zs[z_i]
            i += 1

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * e
        if e2 >= dy:
            e += dy
            x0 += sx
        if e2 <= dx:
            e += dx
            y0 += sy
        z_i += 1
    return i


def _fill_span(
    edge_pts: np.ndarray,
    z_vals: np.ndarray,
    buf: np.ndarray,
    zbuf: np.ndarray,
    intensity: float = 1.0,
):
    h, w = buf.shape

    for y in np.unique(edge_pts[:, 1]):
        y_ind = edge_pts[:, 1] == y
        pts = edge_pts[y_ind]
        sort_ind = pts[:, 0].argsort()
        pts = pts[sort_ind]

        zs = z_vals[y_ind][sort_ind]

        if len(pts) == 1:
            x, z = pts[0][0], zs[0]
            if 0 <= x < w and 0 <= y < h and z > zbuf[y, x]:
                buf[y, x] = intensity
                zbuf[y, x] = z
        else:
            x0, x1 = pts[0, 0], pts[-1, 0]
            xs = np.arange(x0, x1 + 1)
            z0, z1 = zs[0], zs[-1]
            zspace = np.linspace(z0, z1, x1 - x0 + 1)

            mask = (0 <= xs) & (xs < w) & (zspace > zbuf[y, xs])
            buf[y, xs[mask]] = intensity
            zbuf[y, xs[mask]] = zspace[mask]
