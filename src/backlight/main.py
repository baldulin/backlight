import argparse
import sys
from math import ceil
from pathlib import Path


def read_file(path):
    with open(path, "r") as f:
        return f.read()
def write_file(path, value):
    with open(path, "w") as f:
        f.write(str(value))


parser = argparse.ArgumentParser(
    prog='Backlight',
    description='Change backlight level',
)

parser.add_argument('-l', '--levels', type=int, default=10)
parser.add_argument('-L', '--lowest', action="store_true")
parser.add_argument('-i', '--increment', action="store_true")
parser.add_argument('-d', '--decrement', action="store_true")
parser.add_argument('-p', '--path', type=Path, default="/sys/class/backlight/")
parser.add_argument('-m', '--min', action="store_true")
parser.add_argument('-M', '--max', action="store_true")
parser.add_argument('-D', '--dir', action="store_true")



def run():
    args = parser.parse_args()
    path = args.path

    if not (path / "brightness").exists():
        for name in path.glob("*"):
            if (path / name / "brightness").exists():
                path = path / name
                break
        else:
            sys.exit(1)

    if args.dir:
        print(path / "brightness")
        sys.exit(0)

    if path / "brightness":
        current_level = int(read_file(path / "brightness"))
        max_brightness = int(read_file(path / "max_brightness"))
        steps = ceil(max_brightness / args.levels)

        if args.increment:
            brightness = min(current_level + steps, max_brightness)
        elif args.decrement:
            brightness = current_level - steps

            if args.lowest:
                if brightness <= 0:
                    if current_level > 1:
                        brightness = 1
                    else:
                        brightness = 0
            else:
                if brightness < 0:
                    brightness = 0
        elif args.max:
            brightness = max_brightness
        elif args.min:
            brightness = 0
        else:
            sys.exit(0)

        write_file(path / "brightness", brightness)


if __name__ == "__main__":
    run()
