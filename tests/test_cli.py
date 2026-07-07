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


def test_cli_repeat_prints_greeting_n_times():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--repeat", "3"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.splitlines() == ["Hello, World!"] * 3


def test_cli_repeat_composes_with_name_and_shout():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--repeat", "2", "--name", "Ada", "--shout"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.splitlines() == ["HELLO, ADA!"] * 2


def test_cli_repeat_zero_is_bad_usage():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--repeat", "0"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip() != ""


def test_cli_repeat_negative_is_bad_usage():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--repeat", "-1"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip() != ""


def test_cli_repeat_non_integer_is_bad_usage():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--repeat", "abc"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip() != ""


def test_cli_farewell_swaps_hello_for_goodbye():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--farewell"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "Goodbye, World!"


def test_cli_farewell_composes_with_name():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--farewell", "--name", "Ada"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "Goodbye, Ada!"


def test_cli_farewell_composes_with_shout():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--farewell", "--shout"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "GOODBYE, WORLD!"


def test_cli_farewell_composes_with_name_and_shout():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dogfood_dev",
            "--farewell",
            "--name",
            "ada",
            "--shout",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "GOODBYE, ADA!"
