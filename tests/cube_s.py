from tge.engine import GraphicsEngine
from tge.model import load_model
from tge.camera import Camera, Projection
from tge.lights import DirectionalLight
from tge.util import Vec3, build_rotation_deg, build_scale, Axis
from tge.display import clear
import time

if __name__ == "__main__":
    engine = GraphicsEngine((100, 50))

    cube = load_model("tests/models/cube.obj")
    cube.apply_transform(build_scale(5, 5, 5))
    cube.apply_transform(build_rotation_deg(45, Axis.Y))
    cube.apply_transform(build_rotation_deg(45, Axis.X))
    engine.add_model(cube)

    FOV = 1.0472
    aspect_ratio = 2
    near_plane = 0.1
    far_plane = 100
    engine.add_camera(
        Camera(Vec3(0, 0, 30), Vec3(0, 0, 0), Vec3(0, 1, 0), FOV, near_plane, far_plane)
    )

    engine.add_light(DirectionalLight(Vec3(0, 0, -1)))

    engine.render(0, Projection.PERSPECTIVE)
    # try:
    #     while True:
    #         engine.display.render_buffer()
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     clear()
    #     print("Test terminated.")
