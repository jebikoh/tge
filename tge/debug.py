"""
This file contains various methods used for visualization and debugging.
"""
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from tge.camera import Camera
from .model import Model
from .util import Vec3


class AxisScale(Enum):
    """Enum for specifying axis scale"""

    LINEAR = "linear"
    LOG = "log"


def plot_scene(model: Model, camera: Camera, title: str = "Scene"):
    """Uses matplotlib to plot a model and a camera in a 3D scatterplot. Used for debugging purposes. Camera position is red, camera direction is blue, and camera up is green.

    Args:
        model (Model): Model to plot
        camera (Camera): Camera to plot
        title (str, optional): Graph title. Defaults to "Scene".
    """
    vertices = model.v[:, :-1]

    edges = set()
    for face in model.f:
        v0, v1, v2 = face
        edges.add((v0, v1))
        edges.add((v1, v2))
        edges.add((v2, v0))
    edges = list(edges)

    # Create a figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Plot the vertices
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2])

    # Plot the edges
    for edge in edges:
        ax.plot(
            [vertices[edge[0], 0], vertices[edge[1], 0]],
            [vertices[edge[0], 1], vertices[edge[1], 1]],
            [vertices[edge[0], 2], vertices[edge[1], 2]],
        )

    # Plot the camera
    if camera is not None:
        ax.scatter(
            camera.pos.v[0],
            camera.pos.v[1],
            camera.pos.v[2],
            c="red",
            label="camera",
        )
        toward = camera.pos.v + camera.dir.v
        ax.scatter(
            toward[0],
            toward[1],
            toward[2],
            c="blue",
            label="dir",
        )
        up = camera.pos.v + camera.up.v
        ax.scatter(
            up[0],
            up[1],
            up[2],
            c="green",
            label="up",
        )

    # Set labels for the axes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")  # type: ignore

    # Show the plot
    plt.title(title)
    plt.show()


def pixel_map(buf: np.ndarray, path: str = "pixel_map.png"):
    plt.imshow(buf, cmap="gray", vmin=0, vmax=1)
    plt.savefig(path)
