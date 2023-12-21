import argparse
from tge.engine import GraphicsEngine
from tge.model import load_model
from tge.camera import Camera, Projection
from tge.lights import DirectionalLight
from tge.util import build_scale, build_rotation_deg, Axis, Vec3
from tge.display import clear
import time


def a_dir():
    parser = argparse.ArgumentParser(
        description="Render a model with directional lighting from camera direction"
    )

    parser.add_argument("model_path", help="Path to model .obj")

    # Transform args
    parser.add_argument(
        "-sXYZ",
        "--scaleXYZ",
        type=float,
        default=10.0,
        help="Scale factor for X, Y, and Z axes (default: 10.0)",
        required=False,
    )

    # Animation args
    parser.add_argument(
        "-rdeg",
        "--rotationDeg",
        type=float,
        help="How much to rotate per frame (degrees)",
        default=2.0,
        required=False,
    )

    # Display args
    parser.add_argument(
        "-dw",
        "--width",
        type=int,
        default=100,
        help="Display width (default: 100)",
        required=False,
    )

    parser.add_argument(
        "-dh",
        "--height",
        type=int,
        default=50,
        help="Display height (default: 50)",
        required=False,
    )

    # Camera args
    parser.add_argument(
        "-fv",
        "--fov",
        type=float,
        default=1.0472,
        help="Camera field of view (default: 1.0472)",
        required=False,
    )

    parser.add_argument(
        "-n",
        "--near",
        type=float,
        default=0.1,
        help="Near plane (default: 0.1)",
        required=False,
    )

    parser.add_argument(
        "-f",
        "--far",
        type=float,
        default=100.0,
        help="Far plane (default: 100.0)",
        required=False,
    )

    parser.add_argument(
        "-fps",
        "--framesPerSecond",
        type=int,
        default=60,
        help="Frames per second (default: 60)",
        required=False,
    )

    args = parser.parse_args()

    engine = GraphicsEngine((args.width, args.height))

    # Models
    model = load_model(args.model_path)
    model.apply_transform(build_scale(args.scaleXYZ, args.scaleXYZ, args.scaleXYZ))
    engine.add_model(model)

    # Camera
    FOV = args.fov
    near_plane = args.near
    far_plane = args.far
    engine.add_camera(
        Camera(Vec3(0, 0, 30), Vec3(0, 0, 0), Vec3(0, 1, 0), FOV, near_plane, far_plane)
    )

    engine.add_light(DirectionalLight(Vec3(0, 0, -1)))

    # Action
    try:
        rot_X = build_rotation_deg(args.rotationDeg, Axis.X)
        rot_Y = build_rotation_deg(args.rotationDeg, Axis.Y)
        rot_Z = build_rotation_deg(args.rotationDeg, Axis.Z)
        t = 1.0 / args.framesPerSecond
        while True:
            model.apply_transform(rot_X)
            model.apply_transform(rot_Y)
            model.apply_transform(rot_Z)
            engine.render(0, Projection.PERSPECTIVE)
            engine.display.render_buffer()
            time.sleep(t)
    except KeyboardInterrupt:
        clear()
        print("Test terminated.")


if __name__ == "__main__":
    a_dir()
