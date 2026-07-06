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
    assert result.stdout.strip() == "HELLO, WORLD!"


def test_cli_shout_composes_with_name():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--name", "ada", "--shout"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "HELLO, ADA!"


def test_cli_unknown_flag_usage_error():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--bogus"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip() != ""
