import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="dogfood-dev")
    parser.add_argument("--name", default="World")
    parser.add_argument("--shout", action="store_true")
    args = parser.parse_args()
    greeting = f"Hello, {args.name}!"
    if args.shout:
        greeting = greeting.upper()
    print(greeting)
