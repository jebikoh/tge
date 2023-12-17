from tge.engine import GraphicsEngine
from tge.model import load_model
from tge.camera import Camera, Projection
from tge.util import Vec3, build_rotation_deg, build_scale, Axis
from tge.lights import DirectionalLight
from tge.display import clear
from tge.debug import pixel_map
import time
import numpy as np

if __name__ == "__main__":
    engine = GraphicsEngine((200, 150))

    # Models
    cube = load_model("tests/models/sphere.obj")
    cube.apply_transform(build_scale(12, 12, 12))
    engine.add_model(cube)

    # Camera
    FOV = 1.0472
    near_plane = 0.1
    far_plane = 100
    engine.add_camera(
        Camera(Vec3(0, 0, 30), Vec3(0, 0, 0), Vec3(0, 1, 0), FOV, near_plane, far_plane)
    )

    # Lights
    engine.add_light(DirectionalLight(Vec3(0, 0, -1)))

    # Action
    engine.render(0, Projection.PERSPECTIVE, debug=False)
    pixel_map(engine.display.debug_buf)
