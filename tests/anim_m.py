from tge.engine import GraphicsEngine
from tge.model import load_model
from tge.camera import Camera, Projection
from tge.util import Axis, Vec3, build_rotation_deg, build_scale
from tge.lights import DirectionalLight
from tge.display import clear
import time
import numpy as np

if __name__ == "__main__":
    engine = GraphicsEngine((100, 50))

    # Models
    model = load_model("tests/models/taurus.obj")
    model.apply_transform(build_scale(10, 10, 10))
    engine.add_model(model)

    # Camera
    FOV = 1.0472
    near_plane = 0.1
    far_plane = 100
    engine.add_camera(
        Camera(Vec3(0, 0, 30), Vec3(0, 0, 0), Vec3(0, 1, 0), FOV, near_plane, far_plane)
    )

    engine.add_light(DirectionalLight(Vec3(0, 0, -1)))

    # Action
    try:
        while True:
            model.apply_transform(build_rotation_deg(2, Axis.X))
            model.apply_transform(build_rotation_deg(2, Axis.Y))
            model.apply_transform(build_rotation_deg(2, Axis.Z))
            engine.render(0, Projection.PERSPECTIVE)
            engine.display.render_buffer()
            time.sleep(0.01)
    except KeyboardInterrupt:
        clear()
        print("Test terminated.")
