from engine import GraphicsEngine
from model import load_model
from util import build_scale
import time


def main():
    e = GraphicsEngine((50, 30))
    cube = load_model("models/cube.obj")
    print(cube.v)

    m_id = e.add_model(cube)
    start = time.time()
    e.transform_model(m_id, build_scale(2, 2, 2))
    end = time.time()

    print(e.models[m_id].v)
    print(f"Time taken: {end - start}")


if __name__ == "__main__":
    main()
