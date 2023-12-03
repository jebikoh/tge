from util import Vec3
from scene import Camera, Projection
import numpy as np


def test_view_matrix():
    camera_position = Vec3(0, 0, 5)
    camera_direction = Vec3(0, 0, -1)  # Looking towards the origin
    camera_up = Vec3(0, 1, 0)

    camera = Camera(
        camera_position, camera_direction, camera_up, fov=60, near=0.1, far=1000
    )
    view_matrix = camera.get_view_matrix()

    assert not np.array_equal(view_matrix, np.identity(4))


def test_projection_matrix():
    aspect_ratio = 16 / 9
    camera = Camera(
        Vec3(0, 0, 5), Vec3(0, 0, -1), Vec3(0, 1, 0), fov=60, near=0.1, far=1000
    )

    proj_matrix = camera.get_proj_matrix(aspect_ratio, Projection.PERSPECTIVE)

    assert not np.array_equal(proj_matrix, np.identity(4))


if __name__ == "__main__":
    test_view_matrix()
    test_projection_matrix()
    print("Tests passed!")
