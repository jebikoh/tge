"""
This file contains various methods used for visualization and debugging.
"""
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from .model import Model
from .util import Vec3


class AxisScale(Enum):
    LINEAR = "linear"
    LOG = "log"


def plot_scatter(
    model: Model,
    c_pos: Vec3,
    x_scale=AxisScale.LINEAR,
    y_scale=AxisScale.LINEAR,
    z_scale=AxisScale.LINEAR,
):
    """Uses matplotlib to plot a model and a camera in a 3D scatterplot. Used for debugging purposes.

    Args:
        model (Model): model to plot
        c_pos (Vec3): camera position
        x_scale (_type_, optional): x axis scale. Defaults to AxisScale.LINEAR.
        y_scale (_type_, optional): y axis scale. Defaults to AxisScale.LINEAR.
        z_scale (_type_, optional): z axis scale. Defaults to AxisScale.LINEAR.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    x = model.v[:, 0]
    y = model.v[:, 1]
    z = model.v[:, 2]
    ax.scatter(x, y, z)

    ax.scatter(
        c_pos.v[0],
        c_pos.v[1],
        c_pos.v[2],
        c="red",
        label="c_pos",
    )

    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")
    ax.set_zlabel("Z Label")  # type: ignore

    ax.set_xscale(x_scale.value)
    ax.set_yscale(y_scale.value)
    ax.set_zscale(z_scale.value)  # type: ignore
    plt.show()


def plot_scene(model: Model, camera: Vec3 | None = None):
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
            camera.v[0],
            camera.v[1],
            camera.v[2],
            c="red",
            label="camera",
        )

    # Set labels for the axes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")  # type: ignore

    # Show the plot
    plt.show()
