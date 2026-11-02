"""Isolated local Chromium smoke; fixed synthetic build, no user browser profile."""

import argparse
import http.server
import json
import shutil
import subprocess
import threading
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BROWSER = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
PROBE = r"""
const pause = () => new Promise(r => setTimeout(r, 150));
window.addEventListener('load', async () => {
  const result = {width: innerWidth, views: [], focusMoved: false, focusReturned: false};
  try {
    for (let i=0; i<40 && !document.querySelector('.dojo-explorer-nav'); i++) await pause();
    for (const name of ['Overview','Compare','Runs','Method']) {
      const button = [...document.querySelectorAll('.dojo-explorer-nav button')].find(b=>b.textContent.trim()===name);
      button.click(); await pause(); await pause();
      const view = document.querySelector('.explorer-view:not([hidden])');
      result.views.push({name, overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
        active: button.getAttribute('aria-current')==='page',
        overflowElements: [...view.querySelectorAll('*')].filter(e=>!e.closest('.table-scroll') && e.getBoundingClientRect().width>0 && e.getBoundingClientRect().right>document.documentElement.clientWidth+1).slice(0,8).map(e=>({tag:e.tagName, className:e.className, text:e.textContent.slice(0,80)})),
        chartWidths: [...view.querySelectorAll('.recharts-wrapper > svg.recharts-surface')].map(s=>s.getBoundingClientRect().width),
        regionWidths: [...view.querySelectorAll('.table-scroll')].map(s=>s.getBoundingClientRect().width)});
    }
    [...document.querySelectorAll('.dojo-explorer-nav button')].find(b=>b.textContent.trim()==='Runs').click(); await pause();
    const trigger = [...document.querySelectorAll('button')].find(b=>b.textContent.trim().startsWith('Details'));
    trigger.click(); await pause();
    result.focusMoved = document.activeElement?.id === 'run-detail-heading';
    [...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='Close details').click(); await pause();
    result.focusReturned = document.activeElement===trigger;
    const summary = document.querySelector('.dataset-details__summary');
    result.disclosureDisplay = getComputedStyle(summary).display;
    result.disclosureHeight = summary.getBoundingClientRect().height;
    result.complete = true;
    window.scrollTo(0,0);
  } catch { result.complete=false; }
  const output=document.createElement('pre'); output.id='browser-check-result';
  output.hidden=true;
  output.textContent=JSON.stringify(result); document.body.append(output);
});
"""


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "data/runtime/browser-ui-v3")
    folder = parser.parse_args().output.resolve()
    folder.mkdir()  # Existing reports/screenshots are preserved.
    shutil.copytree(ROOT / "dashboard/dist", folder / "site")
    site = folder / "site"
    index = (site / "index.html").read_text(encoding="utf-8")
    (site / "index.html").write_text(index.replace(
        "</body>", '<script src="./probe.js"></script></body>'), encoding="utf-8")
    (site / "probe.js").write_text(PROBE, encoding="utf-8")
    browser = BROWSER if BROWSER.is_file() else Path(
        "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
    reports = []
    handler = partial(QuietHandler, directory=str(site))
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            result = subprocess.run([
                "node", str(ROOT / "scripts/dashboard_browser_probe.mjs"), str(browser), str(folder),
                f"http://127.0.0.1:{server.server_port}/"], check=False, capture_output=True, timeout=90)
            if result.returncode:
                raise RuntimeError("browser_probe_incomplete")
            reports = json.loads(result.stdout)
        finally:
            server.shutdown()
    (folder / "report.json").write_text(json.dumps(reports, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(reports))
    return 0 if all(r.get("complete") and r["width"] == r["requested_width"]
                    and len(r["views"]) == 4
                    and all(not v["overflow"] and v["active"] for v in r["views"])
                    and any(v["name"] == "Compare" and any(w > 100 for w in v["chartWidths"])
                            for v in r["views"])
                    and r["disclosureDisplay"] == "list-item" and r["disclosureHeight"] >= 44
                    and r["tableKeyboardScroll"]["focused"] and r["tableKeyboardScroll"]["focusVisible"]
                    and r["tableKeyboardScroll"]["outlineWidth"] >= 2
                    and (not r["tableKeyboardScroll"]["needed"] or r["tableKeyboardScroll"]["scrolled"])
                    and all(r["keyboardNavigation"].values())
                    and ("largeText" not in r or (r["largeText"]["rootScale"] >= 1.99
                         and all(not view["overflow"] for view in r["largeText"]["views"])))
                    and r["focusMoved"] and r["focusReturned"] for r in reports) else 2


if __name__ == "__main__":
    raise SystemExit(main())
