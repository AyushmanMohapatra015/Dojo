"""Method-level pytest receipts with explicit nested-subtest aggregation.

Standalone collector only; not connected to either frozen v1 Docker runner.
SubtestReport detection is tested against pinned pytest 9.1.1.
"""


class ReceiptV2:
    def __init__(self):
        self.items = {}
        self.errors = set()
        self.collection_finished = False

    def pytest_collection_finish(self, session):
        if self.collection_finished:
            self.errors.add("duplicate_collection_finish")
        self.collection_finished = True
        for item in session.items:
            if item.nodeid in self.items:
                self.errors.add(item.nodeid)
            self.items[item.nodeid] = {"phases": {}, "outcomes": set(),
                                       "subtests": {"passed": 0, "failed": 0, "skipped": 0}}

    def pytest_collectreport(self, report):
        # A skipped module supplies no collected methods to account for safely.
        if report.failed or report.skipped:
            self.errors.add(report.nodeid)

    def pytest_runtest_logreport(self, report):
        from _pytest.subtests import SubtestReport

        node = report.nodeid
        if node not in self.items:
            self.errors.add(node)
            return
        state = self.items[node]
        outcome, phase = report.outcome, report.when
        if outcome not in {"passed", "failed", "skipped"} or phase not in {
                "setup", "call", "teardown"}:
            self.errors.add(node)
            return
        if isinstance(report, SubtestReport):
            if phase != "call":
                self.errors.add(node)
                return
            state["subtests"][outcome] += 1
            state["outcomes"].add(outcome)
            return
        if phase in state["phases"]:
            self.errors.add(node)
        state["phases"][phase] = outcome
        if phase == "call" or outcome != "passed":
            state["outcomes"].add(outcome)
        if phase != "call" and outcome == "failed":
            self.errors.add(node)

    def report(self, exit_code):
        errors = set(self.errors)
        result = {key: [] for key in ("passed", "failed", "skipped")}
        if not self.collection_finished:
            errors.add("missing_collection_finish")
        for node, state in self.items.items():
            phases, outcomes = state["phases"], state["outcomes"]
            # Passing subtests cannot stand in for a missing parent call/teardown.
            expected = {"setup", "teardown"}
            if phases.get("setup") == "passed":
                expected.add("call")
            if set(phases) != expected or not outcomes:
                errors.add(node)
            if node in errors:
                continue
            status = ("failed" if "failed" in outcomes else
                      "skipped" if "skipped" in outcomes else "passed")
            result[status].append(node)
        return {"collector_protocol": "method-subtests-v2", "exit_code": int(exit_code),
                "collected": len(self.items),
                **{key: sorted(value) for key, value in result.items()},
                "errors": sorted(errors),
                "subtests": {node: dict(state["subtests"]) for node, state in sorted(self.items.items())
                             if sum(state["subtests"].values())}}
