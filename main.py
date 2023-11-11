from display import Display, clear
import time


def main():
    display = Display(25, 25)
    try:
        while True:
            display.render()
            time.sleep(1)  # Reduce CPU usage
            # Update buffer content here if needed
    except KeyboardInterrupt:
        clear()
        print("Program terminated.")


if __name__ == "__main__":
    main()
