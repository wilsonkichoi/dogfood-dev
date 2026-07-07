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


def _non_negative_int(value: str) -> int:
    """Parse `--pad`'s value: N literal spaces applied symmetrically on both sides."""
    try:
        result = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid non-negative int value: {value!r}")
    if result < 0:
        raise argparse.ArgumentTypeError(f"invalid non-negative int value: {value!r}")
    return result


_ANSI_RESET = "\x1b[0m"
_COLOR_CODES = {
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "blue": "\x1b[34m",
    "yellow": "\x1b[33m",
}


def main() -> None:
    parser = _ArgumentParser(prog="dogfood-dev")
    parser.add_argument("--name", default="World")
    parser.add_argument("--shout", action="store_true")
    parser.add_argument("--farewell", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--repeat", type=_positive_int, default=1)
    group.add_argument("--json", action="store_true")
    parser.add_argument("--color", choices=sorted(_COLOR_CODES))
    parser.add_argument("--pad", type=_non_negative_int, default=0)
    args = parser.parse_args()
    salutation = "Goodbye" if args.farewell else "Hello"
    greeting = f"{salutation}, {args.name}!"
    if args.shout:
        greeting = greeting.upper()
    if args.pad:
        greeting = f"{' ' * args.pad}{greeting}{' ' * args.pad}"
    if args.color:
        greeting = f"{_COLOR_CODES[args.color]}{greeting}{_ANSI_RESET}"
    if args.json:
        print(json.dumps({"message": greeting}))
        return
    for _ in range(args.repeat):
        print(greeting)
