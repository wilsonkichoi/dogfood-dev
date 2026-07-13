import json
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

def test_cli_upper_uppercases_name():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--upper"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "Hello, WORLD!"


def test_cli_upper_composes_with_name():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--name", "ada", "--upper"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "Hello, ADA!"

def test_cli_exclaim_appends_three_exclamation_marks():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--exclaim"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "Hello, World!!!"


def test_cli_exclaim_composes_with_name():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--name", "Ada", "--exclaim"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "Hello, Ada!!!"


def test_cli_exclaim_composes_with_shout():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--exclaim", "--shout"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout == "HELLO, WORLD!!!\n"


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


def test_cli_color_red_wraps_greeting():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--color", "red"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.rstrip("\n") == "\x1b[31mHello, World!\x1b[0m"


def test_cli_color_green_wraps_greeting():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--color", "green"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.rstrip("\n") == "\x1b[32mHello, World!\x1b[0m"


def test_cli_color_blue_wraps_greeting():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--color", "blue"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.rstrip("\n") == "\x1b[34mHello, World!\x1b[0m"


def test_cli_color_yellow_wraps_greeting():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--color", "yellow"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.rstrip("\n") == "\x1b[33mHello, World!\x1b[0m"


def test_cli_color_invalid_value_is_bad_usage():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--color", "purple"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip() != ""


def test_cli_color_composes_with_name():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--color", "red", "--name", "Ada"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.rstrip("\n") == "\x1b[31mHello, Ada!\x1b[0m"


def test_cli_color_composes_with_shout():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--color", "green", "--shout"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.rstrip("\n") == "\x1b[32mHELLO, WORLD!\x1b[0m"


def test_cli_color_composes_with_name_and_shout():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dogfood_dev",
            "--color",
            "blue",
            "--name",
            "Ada",
            "--shout",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.rstrip("\n") == "\x1b[34mHELLO, ADA!\x1b[0m"


def test_cli_reverse_reverses_greeting():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--reverse"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "!dlroW ,olleH"


def test_cli_reverse_composes_with_name():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--reverse", "--name", "Ada"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "!adA ,olleH"


def test_cli_reverse_composes_with_shout():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--reverse", "--shout"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "!DLROW ,OLLEH"


def test_cli_reverse_composes_with_name_and_shout():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--reverse", "--name", "Ada", "--shout"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "!ADA ,OLLEH"


def test_cli_json_emits_json_message():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout) == {"message": "Hello, World!"}


def test_cli_json_incompatible_with_repeat_is_bad_usage():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--json", "--repeat", "2"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip() != ""


def test_cli_json_composes_with_name_and_shout():
    result = subprocess.run(
        [sys.executable, "-m", "dogfood_dev", "--json", "--name", "Ada", "--shout"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout) == {"message": "HELLO, ADA!"}
