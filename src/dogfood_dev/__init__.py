import argparse
import json


class _ArgumentParser(argparse.ArgumentParser):
    """Prints a concise one-line usage message to stderr on bad usage."""

    def error(self, message: str) -> None:
        self.exit(
            2,
            f"{self.prog}: error: {message} "
            f"(run '{self.prog} --help' to see available options)\n",
        )


def _positive_int(value: str) -> int:
    try:
        result = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid positive int value: {value!r}")
    if result < 1:
        raise argparse.ArgumentTypeError(f"invalid positive int value: {value!r}")
    return result


def main() -> None:
    parser = _ArgumentParser(prog="dogfood-dev")
    parser.add_argument("--name", default="World")
    parser.add_argument("--shout", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--repeat", type=_positive_int, default=1)
    group.add_argument("--json", action="store_true")
    args = parser.parse_args()
    greeting = f"Hello, {args.name}!"
    if args.shout:
        greeting = greeting.upper()
    if args.json:
        print(json.dumps({"message": greeting}))
        return
    for _ in range(args.repeat):
        print(greeting)
