import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="dogfood-dev")
    parser.add_argument("--name", default="World")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")
