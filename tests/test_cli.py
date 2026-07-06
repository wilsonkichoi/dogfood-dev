import subprocess
import sys


def test_cli_prints_hello_world():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "Hello, World!"


def test_cli_prints_custom_name():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--name", "Ada"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "Hello, Ada!"


def test_cli_shout_uppercases_greeting():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--shout"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "hello, world!"


def test_cli_shout_composes_with_name():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--name", "ada", "--shout"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "hello, ada!"
