import os


def clear_dir(path: str):
    if os.path.exists(path) and os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            if os.path.isfile(os.path.join(path, file)):
                os.remove(os.path.join(path, file))
