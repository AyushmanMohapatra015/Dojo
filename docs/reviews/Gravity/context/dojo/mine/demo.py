"""Create an isolated, synthetic two-commit history for learning (not benchmark data)."""

import subprocess
from pathlib import Path

BASE_SOURCE = "def add(a, b):\n    return a - b\n"
FIX_SOURCE = "def add(a, b):\n    return a + b\n"
BASE_TEST = "from calculator import add\n\n\ndef test_zero():\n    assert add(0, 0) == 0\n"
NEW_TEST = "\n\ndef test_positive_numbers():\n    assert add(2, 3) == 5\n"


def create_demo(repo: Path) -> None:
    """Only create a new directory; never alter the owner's existing repository."""
    repo.mkdir(parents=True, exist_ok=False)

    def run(*args: str) -> None:
        subprocess.run(
            ["git", "-c", "safe.directory=" + str(repo.resolve()),
             "-c", "core.hooksPath=" + str((repo / ".disabled-hooks").resolve()),
             "-c", "commit.gpgSign=false", "-c", "user.name=Dojo Demo",
             "-c", "user.email=demo@example.invalid", "-C", str(repo), *args],
            check=True, capture_output=True, timeout=30,
        )

    run("init", "--template=", "--initial-branch=main")
    (repo / "tests").mkdir()
    (repo / "calculator.py").write_text(
        BASE_SOURCE, encoding="utf-8",
    )
    test = repo / "tests" / "test_calculator.py"
    test.write_text(BASE_TEST, encoding="utf-8")
    run("add", "--", "calculator.py", "tests/test_calculator.py")
    run("commit", "-m", "Synthetic base: addition has a bug")
    (repo / "calculator.py").write_text(
        FIX_SOURCE, encoding="utf-8",
    )
    with test.open("a", encoding="utf-8") as stream:
        stream.write(NEW_TEST)
    run("add", "--", "calculator.py", "tests/test_calculator.py")
    run("commit", "-m", "Synthetic fix: add positive numbers correctly")
