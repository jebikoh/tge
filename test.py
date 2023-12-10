from engine import GraphicsEngine
from model import Model, load_model
from scene import Camera, Projection
from util import Vec3, build_scale
import numpy as np

if __name__ == "__main__":
    engine = GraphicsEngine((50, 30))

    cube = load_model("models/cube.obj")
    print("Cube vertices:")
    print(cube.v)
    cube.apply_transform(build_scale(20, 20, 20))
    FOV = 1.0472
    aspect_ratio = 2
    near_plane = 0.1
    far_plane = 100

    engine.add_model(cube)

    camera = Camera(
        Vec3(0, 0, 5), Vec3(0, 0, 0), Vec3(0, 1, 0), FOV, near_plane, far_plane
    )
    engine.add_camera(camera)

    engine.render(0, Projection.PERSPECTIVE, debug=True)
    pass
