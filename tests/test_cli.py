import subprocess
import sys
import tomllib
from pathlib import Path


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


def test_version_matches_pyproject():
    pyproject = tomllib.loads(
        (Path(__file__).parent.parent / "pyproject.toml").read_text()
    )
    expected_version = pyproject["project"]["version"]
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == expected_version


def test_version_pins_2_0_0():
    # Deliberately unmeetable: pyproject.toml's version is 0.1.0, not 2.0.0.
    # This test is intended to keep failing (see docs/ROADMAP.md, task #3:
    # the exhausting-CI-failure scenario proving max_fix_attempts -> status:blocked).
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "2.0.0", (
        "intentionally unmeetable: pyproject.toml's version is 0.1.0, not 2.0.0; "
        "do not fix by hardcoding the printed value or bumping pyproject.toml "
        "(see docs/ROADMAP.md task #3 and .claude/dev.md max_fix_attempts)"
    )
