#!/usr/bin/env python3
"""Prepare portfolio images: crop, key out flat backgrounds, export responsive WebP.

Optional tool — the site itself is plain static files. Run from the repo root:

    python3 tools/prepare_assets.py

Source renders live in the sibling project repos (/home/tj/<repo>).
"""

from pathlib import Path
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

# name, source path, widths, mode ("keep" | "key")
JOBS = [
    ("ganymede-iso",      "GaNymede/Pics/board-iso.png",              [1800, 1100], "keyblack"),
    ("ganymede-top",      "GaNymede/Pics/board-top.png",              [1400, 900],  "keyblack"),
    ("nano-front",        "nitride-nano/Pics/nitride-nano-f.png",     [1800, 1100], "keyblack"),
    ("nano-back",         "nitride-nano/Pics/nitride-nano-b.png",     [1500, 950],  "keyblack"),
    ("nano-photo",        "nitride-nano/Pics/Assembled.jpg",          [1600, 1000], "keep"),
    ("compressor-front",  "CompressorController/FB.png",              [1500, 950],  "key"),
    ("compressor-back",   "CompressorController/FC.png",              [1500, 950],  "key"),
    ("dab-hero",          "DAB_DCDC/Pictures/DAB9T.png",               [1800, 1100], "keyblack"),
    ("dab-macro",         "DAB_DCDC/Pictures/DAB10.jpg",               [1800, 1100], "keep"),
    ("dab-top",           "DAB_DCDC/Pictures/irlpcb.jpg",              [1600, 1000], "keep"),
    ("dab-cooling",       "DAB_DCDC/Pictures/cooling_4k_H.png",        [1500, 950],  "keyblack"),
    ("twin-gan",          "Twin-GaN/Twin-GaN.png",                     [1400, 900],  "key"),
    ("schroombort",       "schroombort/Pictures/SchroombortRENDER.png",[1500, 950],  "keyblack"),
    ("schroombort-photo", "schroombort/Pictures/schrromfoto.png",      [1500, 950],  "keep"),
]


def border_connected(mask: np.ndarray) -> np.ndarray:
    """Keep only mask pixels reachable from the image border (4-connectivity)."""
    h, w = mask.shape
    seen = np.zeros_like(mask)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if mask[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if mask[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    return seen


def key_black(im: Image.Image) -> Image.Image:
    """Remove a pure-black render backdrop so the board floats on the page."""
    arr = np.asarray(im.convert("RGB")).astype(np.int16)
    raw = (arr[..., 0] < 26) & (arr[..., 1] < 26) & (arr[..., 2] < 26)
    bg = border_connected(raw)
    # stop a couple of pixels short of the artwork: dark board edges survive
    for _ in range(2):
        bg = (bg & np.roll(bg, 1, 0) & np.roll(bg, -1, 0)
                 & np.roll(bg, 1, 1) & np.roll(bg, -1, 1))
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    alpha_im = Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(0.5))
    out = im.convert("RGBA")
    out.putalpha(alpha_im)
    return out


def key_background(im: Image.Image) -> Image.Image:
    """Remove a flat lavender render backdrop, keeping the artwork."""
    arr = np.asarray(im.convert("RGB")).astype(np.int16)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    # Lavender backdrop: blue clearly above red, and reasonably bright.
    raw = ((b - r) > 10) & (b > 105) & (r > 45) & (g < 245)
    raw = raw | ((b > 150) & (r > 150) & (g > 150) & ((b - g) > 6))
    bg = border_connected(raw)
    # Grow the background a couple of pixels so light fringes go with it.
    grown = bg.copy()
    for _ in range(2):
        grown = (
            grown
            | np.roll(grown, 1, 0) | np.roll(grown, -1, 0)
            | np.roll(grown, 1, 1) | np.roll(grown, -1, 1)
        )
    alpha = np.where(grown, 0, 255).astype(np.uint8)
    alpha_im = Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(0.7))
    out = im.convert("RGBA")
    out.putalpha(alpha_im)
    return out


def process(name, rel, widths, mode):
    src = SRC / rel
    if not src.exists():
        print(f"  !! missing {src}")
        return
    im = Image.open(src)
    im = im.convert("RGBA") if mode in ("key", "keyblack") else im.convert("RGB")
    if mode == "key":
        im = key_background(im)
    elif mode == "keyblack":
        im = key_black(im)
    if mode in ("key", "keyblack"):
        box = im.getchannel("A").getbbox()
        if box:
            pad = 6
            box = (max(0, box[0] - pad), max(0, box[1] - pad),
                   min(im.width, box[2] + pad), min(im.height, box[3] + pad))
            im = im.crop(box)
    base_w = im.width
    for w in widths:
        h = round(im.height * w / im.width)
        resized = im.resize((w, h), Image.LANCZOS)
        dest = OUT / f"{name}-{w}.webp"
        if mode in ("key", "keyblack"):
            resized.save(dest, "WEBP", quality=86, method=6)
        else:
            resized.save(dest, "WEBP", quality=80, method=6)
        print(f"  {dest.name:28} {w}x{h}  {dest.stat().st_size // 1024:>4} KB")


for job in JOBS:
    print(job[0])
    process(*job)
print("done ->", OUT)
