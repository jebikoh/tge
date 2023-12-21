import argparse
from tge.engine import GraphicsEngine
from tge.model import load_model
from tge.camera import Camera, Projection
from tge.lights import DirectionalLight
from tge.util import build_scale, build_rotation_deg, Axis, Vec3
from tge.display import clear
import time


def r_dir():
    parser = argparse.ArgumentParser(
        description="Render a model with directional lighting from camera direction"
    )

    parser.add_argument("model_path", help="Path to model .obj")

    # Transform args
    parser.add_argument(
        "-rX",
        "--rotationX",
        type=float,
        help="Rotation around X axis (degrees)",
        required=False,
    )

    parser.add_argument(
        "-rY",
        "--rotationY",
        type=float,
        help="Rotation around Y axis (degrees)",
        required=False,
    )

    parser.add_argument(
        "-rZ",
        "--rotationZ",
        type=float,
        help="Rotation around Z axis (degrees)",
        required=False,
    )

    parser.add_argument(
        "-sXYZ",
        "--scaleXYZ",
        type=float,
        default=10.0,
        help="Scale factor for X, Y, and Z axes (default: 10.0)",
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

    args = parser.parse_args()

    engine = GraphicsEngine((args.width, args.height))

    # Models
    model = load_model(args.model_path)
    model.apply_transform(build_scale(args.scaleXYZ, args.scaleXYZ, args.scaleXYZ))
    if args.rotationX:
        model.apply_transform(build_rotation_deg(args.rotationX, Axis.X))
    if args.rotationY:
        model.apply_transform(build_rotation_deg(args.rotationY, Axis.Y))
    if args.rotationZ:
        model.apply_transform(build_rotation_deg(args.rotationZ, Axis.Z))
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
    engine.render(0, Projection.PERSPECTIVE)
    try:
        while True:
            engine.display.render_buffer()
            time.sleep(1)
    except KeyboardInterrupt:
        clear()
        print("Test terminated.")


if __name__ == "__main__":
    r_dir()
