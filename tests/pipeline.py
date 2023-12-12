from tge.engine import GraphicsEngine
from tge.model import load_model
from tge.scene import Camera, Projection
from tge.util import Vec3, build_scale

if __name__ == "__main__":
    engine = GraphicsEngine((60, 30))

    cube = load_model("tests/models/cube.obj")
    cube.apply_transform(build_scale(10, 10, 10))
    FOV = 1.0472
    aspect_ratio = 2
    near_plane = 0.1
    far_plane = 100

    engine.add_model(cube)

    camera = Camera(
        Vec3(0, 0, 30), Vec3(0, 0, 0), Vec3(0, 1, 0), FOV, near_plane, far_plane
    )
    engine.add_camera(camera)

    engine.render(0, Projection.PERSPECTIVE, debug=True)
