import argparse
from tge.engine import GraphicsEngine
from tge.model import load_model
from tge.camera import Camera, Projection
from tge.lights import DirectionalLight
from tge.util import build_scale, build_rotation_deg, Axis, Vec3
from tge.display import clear
import time


def debug():
    WIDTH = 100
    HEIGHT = 50

    MODEL_PATH = "tests/models/cube.obj"
    SCALE = 5.0
    RX = 25.0
    RY = 45.0
    RZ = 45.0

    FOV = 1.0472
    NEAR = 0.1
    FAR = 100

    engine = GraphicsEngine((WIDTH, HEIGHT))

    # Models
    model = load_model(MODEL_PATH)
    model.apply_transform(build_scale(SCALE, SCALE, SCALE))
    if RX:
        model.apply_transform(build_rotation_deg(RX, Axis.X))
    if RY:
        model.apply_transform(build_rotation_deg(RY, Axis.Y))
    if RZ:
        model.apply_transform(build_rotation_deg(RZ, Axis.Z))
    engine.add_model(model)

    # Camera
    engine.add_camera(
        Camera(Vec3(0, 0, 30), Vec3(0, 0, 0), Vec3(0, 1, 0), FOV, NEAR, FAR)
    )

    engine.add_light(DirectionalLight(Vec3(0, 0, -1)))

    # Action
    engine.render(0, Projection.PERSPECTIVE)
    # try:
    #     while True:
    #         engine.display.render_buffer()
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     clear()
    #     print("Test terminated.")


if __name__ == "__main__":
    debug()
