"""Check explicit CSS palette pairs; not a whole-page accessibility certification."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = (("text", "surface"), ("text", "bg"), ("muted", "surface"), ("muted", "bg"),
         ("accent", "surface"), ("accent", "bg"), ("accent-text", "accent"),
         ("warn-text", "warn-bg"), ("err-text", "err-bg"), ("ok-text", "ok-bg"),
         ("bad-text", "bad-bg"), ("unk-text", "unk-bg"))


def contrast(first, second):
    def luminance(color):
        if re.fullmatch(r"#[0-9a-fA-F]{6}", color) is None:
            raise ValueError("invalid_palette_color")
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return sum(c * weight for c, weight in zip(linear, (0.2126, 0.7152, 0.0722), strict=True))
    low, high = sorted((luminance(first), luminance(second)))
    return (high + 0.05) / (low + 0.05)


def main():
    css = (ROOT / "dashboard/src/styles.css").read_text(encoding="utf-8")
    palette = dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6});", css))
    rows = [{"text": text, "background": background,
             "ratio": contrast(palette[text], palette[background])} for text, background in PAIRS]
    passed = all(row["ratio"] >= 4.5 for row in rows)
    print(json.dumps({"palette_pairs_pass": passed, "minimum_required": 4.5,
                      "pairs": rows, "whole_page_accessibility_verified": False}))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
