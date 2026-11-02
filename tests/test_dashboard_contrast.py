import pytest

from scripts.check_dashboard_contrast import contrast


def test_independent_contrast_oracles():
    assert contrast("#000000", "#ffffff") == 21
    assert contrast("#ffffff", "#ffffff") == 1
    assert contrast("#777777", "#ffffff") == pytest.approx(4.47808945)
    assert contrast("#777777", "#ffffff") < 4.5
    with pytest.raises(ValueError, match="invalid_palette_color"):
        contrast("transparent", "#ffffff")
