import argparse
from importlib.metadata import version


def main() -> None:
    parser = argparse.ArgumentParser(prog="dogfood-dev")
    parser.add_argument("--name", default="World")
    parser.add_argument("--shout", action="store_true")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()
    if args.version:
        print(version("dogfood-dev"))
        return
    greeting = f"Hello, {args.name}!"
    if args.shout:
        greeting = greeting.upper()
    print(greeting)
