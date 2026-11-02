import zipfile
from pathlib import Path

import pytest

from scripts.audit_release_wheel import audit


def wheel(path, extra=None):
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("dojo/__init__.py", "")
        archive.writestr("dojo_demo.dist-info/licenses/LICENSE",
                         (Path(__file__).resolve().parents[1] / "LICENSE").read_bytes())
        if extra:
            archive.writestr(extra, "fictional-content")
    return path


def test_minimal_archive(tmp_path):
    assert audit(wheel(tmp_path / "test.whl"))["license_matches"]


@pytest.mark.parametrize("extra", [".env", "dojo/.env", "data/runtime/test.sqlite3",
                                  "docs/reviews/private.txt", "../escape.py",
                                  "dojo/__pycache__/code.pyc", "dojo/unexpected.json"])
def test_private_or_unexpected_member_refused(tmp_path, extra):
    with pytest.raises(ValueError):
        audit(wheel(tmp_path / "test.whl", extra))
