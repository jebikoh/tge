from typing import List
import numpy as np
from .engine import GraphicsEngine


class Animation:
    def __init__(
        self,
        m: int,
        start: int,
        stop: int,
        r: List[np.ndarray] | np.ndarray | None = None,
        t: np.ndarray | None = None,
        s: np.ndarray | None = None,
    ):
        """Initialize an animation. Rotation matrices must be provided separately per-axis

        Args:
            m (int): Model ID
            start (int): Start frame
            stop (int): Stop frame
            r (List[np.ndarray] | np.ndarray | None): Rotation matrix(s) (4x4)
            t (np.ndarray | None): Translation Matrix (4x4)
            s (np.ndarray | None): Scale Matrix (4x4)

        Raises:
            ValueError: If provided rotation matrix is not 4x4
            ValueError: If provided translation matrix is not 4x4
            ValueError: If provided scale matrix is not 4x4
        """
        if r is not None:
            if isinstance(r, list):
                for i in range(len(r)):
                    if r[i].shape != (4, 4):
                        raise ValueError("Rotation matrix must be 4x4")
            if isinstance(r, np.ndarray) and r.shape != (4, 4):
                raise ValueError("Rotation matrix must be 4x4")
        if t is not None and t.shape != (4, 4):
            raise ValueError("Translation matrix must be 4x4")
        if s is not None and s.shape != (4, 4):
            raise ValueError("Scale matrix must be 4x4")

        self.m = m
        self.start = start
        self.stop = stop
        self.r = r if r is not None else np.eye(4)
        self.t = t if t is not None else np.eye(4)
        self.s = s if s is not None else np.eye(4)

    def get_transform(self, frame: int) -> np.ndarray:
        """Get the transformation matrix for a given frame

        Args:
            frame (int): Frame to get transformation for

        Raises:
            ValueError: If frame is out of range

        Returns:
            np.ndarray: Transformation matrix (4x4)
        """
        if frame < self.start or frame > self.stop:
            raise ValueError("Frame out of range")


class AnimationManager:
    def __init__(self, engine: GraphicsEngine):
        """Initialize an animation manager

        Args:
            engine (GraphicsEngine): Graphics engine
        """
        self.engine: GraphicsEngine = engine
        self.animations: List[Animation] = []

    def add_animations(self, animations: list[Animation] | Animation):
        """Add animations to the manager

        Args:
            animations (list[Animation]): Animations to add
        """
        if isinstance(animations, Animation):
            self.animations.append(animations)
        else:
            self.animations.extend(animations)
