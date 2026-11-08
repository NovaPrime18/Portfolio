#!/usr/bin/env python3
"""Render the site to PNGs for design review.

    PYTHONPATH=.pylibs python3 tools/shoot.py [page ...] [--mobile]

Reduced-motion is emulated so scroll-reveal content is visible in stills.
Output goes to .preview/
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".preview"
OUT.mkdir(exist_ok=True)

# Set PLAYWRIGHT_CHROME to a chrome/chromium/headless-shell binary if Playwright
# cannot find its own; otherwise it launches whatever it installed.
CHROME = os.environ.get("PLAYWRIGHT_CHROME")

args = [a for a in sys.argv[1:] if not a.startswith("--")]
mobile = "--mobile" in sys.argv

pages = args or ["index.html"]
if not pages:
    pages = ["index.html"]

with sync_playwright() as p:
    launch = {"args": ["--no-sandbox", "--font-render-hinting=none"]}
    if CHROME and Path(CHROME).exists():
        launch["executable_path"] = CHROME
    browser = p.chromium.launch(**launch)
    for page in pages:
        src = ROOT / page
        stem = src.stem
        if mobile:
            ctx = browser.new_context(
                viewport={"width": 390, "height": 844},
                device_scale_factor=2,
                is_mobile=True,
                has_touch=True,
                reduced_motion="reduce",
            )
            suffix = "-mobile"
        else:
            ctx = browser.new_context(
                viewport={"width": 1440, "height": 1000},
                device_scale_factor=1,
                reduced_motion="reduce",
            )
            suffix = ""
        pg = ctx.new_page()
        pg.goto(src.as_uri())
        pg.wait_for_timeout(350)
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(500)
        pg.evaluate("window.scrollTo(0, 0)")
        pg.wait_for_timeout(350)
        height = pg.evaluate("document.documentElement.scrollHeight")
        dest = OUT / f"{stem}{suffix}.png"
        pg.screenshot(path=str(dest), full_page=True)
        print(f"{dest.name}  1440x{height}" if not mobile else f"{dest.name}  390x{height}")
        ctx.close()
    browser.close()
