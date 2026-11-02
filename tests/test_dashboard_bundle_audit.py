"""Public static build shape rejects private artifacts and missing offline policy."""

import pytest

from scripts.audit_dashboard_bundle import BundleAuditError, audit_bundle


@pytest.fixture
def bundle(tmp_path):
    assets = tmp_path / "assets"
    assets.mkdir()
    (tmp_path / "index.html").write_text(
        "<title>synthetic offline view</title>"
        "<meta http-equiv=\"Content-Security-Policy\" content=\"connect-src 'none'\">",
        encoding="utf-8",
    )
    (assets / "index-abc.js").write_bytes(b"console.log('synthetic')")
    (assets / "index-def.css").write_bytes(b"body{color:#123}")
    return tmp_path


def test_minimal_bundle_passes_without_publication_claim(bundle):
    report = audit_bundle(bundle)
    assert report["asset_count"] == 2
    assert report["ready_to_publish"] is False
    assert report["whole_project_secret_clearance"] is False


@pytest.mark.parametrize("change", ["private_marker", "source_map", "extra_file", "missing_csp"])
def test_private_or_unexpected_output_is_refused(bundle, change):
    js = bundle / "assets/index-abc.js"
    if change == "private_marker":
        js.write_bytes(b"NEBIUS_API_KEY=FICTIONAL_CANARY")
    elif change == "source_map":
        js.write_bytes(b"//# sourceMappingURL=index.js.map")
    elif change == "extra_file":
        (bundle / ".env").write_text("FICTIONAL_CANARY")
    else:
        (bundle / "index.html").write_text("synthetic offline view")
    with pytest.raises(BundleAuditError):
        audit_bundle(bundle)
