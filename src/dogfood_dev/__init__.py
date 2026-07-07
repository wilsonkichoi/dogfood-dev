import argparse


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
    parser.add_argument("--repeat", type=_positive_int, default=1)
    parser.add_argument("--farewell", action="store_true")
    args = parser.parse_args()
    salutation = "Goodbye" if args.farewell else "Hello"
    greeting = f"{salutation}, {args.name}!"
    if args.shout:
        greeting = greeting.upper()
    for _ in range(args.repeat):
        print(greeting)
