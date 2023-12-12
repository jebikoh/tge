from tge.engine import GraphicsEngine
from tge.model import load_model
from tge.camera import Camera, Projection
from tge.util import Vec3, build_scale, build_rotation_deg, Axis
from tge.display import get_terminal_size, clear
import time
import numpy as np

if __name__ == "__main__":
    w, h = get_terminal_size()
    # print(w, h)
    engine = GraphicsEngine((180, 40))

    cube = load_model("tests/models/cube.obj")
    cube.apply_transform(build_scale(5, 5, 5))
    cube.apply_transform(build_rotation_deg(45, Axis.Y))

    FOV = 1.0472
    aspect_ratio = 2
    near_plane = 0.1
    far_plane = 100

    engine.add_model(cube)

    camera = Camera(
        Vec3(0, 0, 30), Vec3(0, 0, 0), Vec3(0, 1, 0), FOV, near_plane, far_plane
    )
    engine.add_camera(camera)
    engine.render(0, Projection.PERSPECTIVE, debug=False)

    try:
        while True:
            engine.display.render_buffer()
            time.sleep(1)
    except KeyboardInterrupt:
        clear()
        print("Test terminated.")
