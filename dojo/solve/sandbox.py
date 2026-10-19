"""Scripted sandbox for offline controller tests. Never executes a command."""

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class FakeStep:
    command: str
    output: str = ""
    exit_code: int | None = 0
    timed_out: bool = False
    patch_after: str | None = None
    visible_tests_pass: bool | None = None

    def __post_init__(self):
        if not isinstance(self.command, str) or not self.command.strip():
            raise ValueError("A scripted command is required")
        if not isinstance(self.output, str) or (
                self.patch_after is not None and not isinstance(self.patch_after, str)):
            raise ValueError("Scripted output and patch must be text")
        if type(self.timed_out) is not bool or (
                self.exit_code is not None and type(self.exit_code) is not int):
            raise ValueError("Invalid scripted exit/timeout state")
        if self.visible_tests_pass is not None and (
                type(self.visible_tests_pass) is not bool or self.timed_out
                or self.exit_code is None or (self.exit_code == 0) != self.visible_tests_pass):
            raise ValueError("Visible-test feedback contradicts command status")


class FakeSandbox:
    """Consumes exact predeclared commands and canned observations, not shell text."""

    def __init__(self, steps: tuple[FakeStep, ...]):
        if any(type(step) is not FakeStep for step in steps):
            raise TypeError("Only scripted fake steps are accepted")
        self.steps = tuple(steps)
        self.commands: list[str] = []
        self.timeouts: list[float] = []
        self.patch = ""
        self.visible_tests_pass: bool | None = None
        self.archive_sha256: str | None = None

    def start(self, archive: bytes):
        if self.archive_sha256 is not None:
            raise RuntimeError("Use a fresh fake sandbox for each simulation")
        self.archive_sha256 = hashlib.sha256(archive).hexdigest()

    def execute(self, command: str, *, timeout: float) -> FakeStep:
        if self.archive_sha256 is None or timeout <= 0:
            raise RuntimeError("Fake sandbox is not ready")
        index = len(self.commands)
        if index >= len(self.steps) or self.steps[index].command != command:
            raise RuntimeError("Command is not in the scripted scenario")
        step = self.steps[index]
        self.commands.append(command)
        self.timeouts.append(timeout)
        if step.patch_after is not None and step.patch_after != self.patch:
            self.patch = step.patch_after
            self.visible_tests_pass = None
        if step.visible_tests_pass is not None:
            self.visible_tests_pass = step.visible_tests_pass
        return step
