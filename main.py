from display import Display, clear
from model import load_model
import time


def main():
    display = Display(50, 30)
    try:
        while True:
            display.render()
            time.sleep(1)
    except KeyboardInterrupt:
        clear()
        print("Program terminated.")


if __name__ == "__main__":
    main()
