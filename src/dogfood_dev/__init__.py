import argparse


class _ArgumentParser(argparse.ArgumentParser):
    """Prints a concise one-line usage message to stderr on bad usage."""

    def error(self, message: str) -> None:
        self.exit(
            2,
            f"{self.prog}: error: {message} "
            f"(run '{self.prog} --help' to see available options)\n",
        )


def main() -> None:
    parser = _ArgumentParser(prog="dogfood-dev")
    parser.add_argument("--name", default="World")
    parser.add_argument("--shout", action="store_true")
    args = parser.parse_args()
    greeting = f"Hello, {args.name}!"
    if args.shout:
        greeting = greeting.upper()
    print(greeting)
