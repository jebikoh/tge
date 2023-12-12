from tge.model import load_model

if __name__ == "__main__":
    cube = load_model("tests/models/cube.obj")
    print(cube.v)
    print(cube.f)
