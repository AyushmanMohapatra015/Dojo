"""Aggregate candidate-panel audit without execution or outcome data."""

from dojo.bench.panel_composition import inspect_candidate_panel


def test_current_candidate_panel_composition(current_stage_b_directory):
    report = inspect_candidate_panel(current_stage_b_directory)
    assert report["schema"] == "dojo-panel-composition-v1"
    assert report["task_count"] == 63
    assert report["counts_by_split"] == {"held_out": 26, "train": 37}
    assert sum(row["count"] for row in report["counts_by_repository"]) == 63
    assert sum(row["count"] for row in report["counts_by_kind"]) == 63
    assert {row["task_kind"] for row in report["counts_by_kind"]} == {
        "api_change", "bug_fix", "compatibility_restore", "feature_request"
    }
    assert report["repeated_issue_fingerprint_groups"] == 0
    assert report["cross_split_issue_fingerprint_groups"] == 0
    assert report["reused_source_archive_groups"] == 6
    assert report["cross_split_source_archive_groups"] >= 0
    assert report["registration_verified"] is False
    assert report["execution_authorized"] is False
    assert report["publishable"] is False
    assert "tasks" not in report and "task_ids" not in report
