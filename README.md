# Portfolio

Personal portfolio for **Thommy** — power electronics, open hardware, and the
tools and enclosures around them.

Live at **https://novaprime18.github.io/Portfolio/**

---

## What this is

A hand-written static site. No framework, no build step, no tracking, no
third-party requests — every font, image and line of CSS is in this repository.
Open `index.html` and it works.

- **Obsidian & gold** visual language, built around the board renders.
- One long homepage, plus a case study for each of six projects.
- Copy is first person; every render is Thommy's own.

## Structure

```
.
├── index.html                      homepage
├── projects/
│   ├── dab-dcdc.html               10 kW dual active bridge
│   ├── ganymede.html               60 V / 100 A GaN motor driver
│   ├── nitride-nano.html           240 W USB-C PD bench supply
│   ├── compressor-controller.html  230 V AC PFC compressor drive
│   ├── twin-gan.html               dual 3-phase GaN controller
│   └── schroombort.html            the 36-key soundboard
├── assets/
│   ├── css/style.css               the whole design system
│   ├── js/main.js                  nav, scroll reveals, copy-email
│   ├── fonts/                      Archivo, Instrument Serif, JetBrains Mono (woff2)
│   ├── img/                        optimised WebP, two widths each
│   ├── src/                        source renders for the local image pipeline
│   ├── logo-mark.svg               monogram used in the header and as a watermark
│   └── favicon.svg / .png          browser and touch icons
├── tools/                          optional authoring helpers, not part of the site
└── .nojekyll                       tells GitHub Pages to serve files as-is
```

## Preview locally

```sh
python3 -m http.server 8000
# http://localhost:8000
```

Opening `index.html` directly works too — there is no routing.

## Deploying (GitHub Pages)

The repository is set up for a project site at `/Portfolio/`:

1. Push to `main`.
2. Repository **Settings → Pages → Build and deployment**:
   **Source: Deploy from a branch**, **Branch: `main`**, **Folder: `/ (root)`**.
3. Wait for the first build; the site appears at
   `https://novaprime18.github.io/Portfolio/`.

All internal links are relative, so the site also works from a user or
organisation page, or any subdirectory.

## Editing

**Text** lives directly in the HTML. Change it and reload.

**Images** are generated from `assets/src/` (or, for older boards, the sibling
project repositories):

```sh
python3 tools/prepare_assets.py
```

It crops, keys out flat black/lavender render backdrops, and writes two WebP
widths per image into `assets/img/`. Edit the `JOBS` table at the top to add a
new board. Requires Pillow and NumPy.

The logo is vector-traced from `assets/src/logo.png`; the header, watermark and
favicon all use the resulting SVG.

**Case-study pages** are produced by `tools/make_cases.py` from one content
dictionary. If you edit a generated page by hand, stop using the generator for
that page — or port the change back into the dictionary first.

**Screenshots for design review** (optional):

```sh
PYTHONPATH=.pylibs python3 tools/shoot.py index.html [--mobile]
```

Needs Playwright and a Chromium build; output lands in `.preview/`.

## Content notes

- Technical figures are taken from each project's README. Where a number is a
  modelled target rather than a measurement, the page says so explicitly.
- Hardware designs are CERN-OHL-S v2.0 unless the project page says otherwise.
- `CompressorController` carries a `© Picobello B.V.` notice in its own
  repository — check that this page's framing matches how that work may be
  represented publicly.

## Colophon

Type: Archivo, Instrument Serif (italic) and JetBrains Mono — all self-hosted,
SIL Open Font License. Colour, spacing and motion live in the CSS custom
properties at the top of `assets/css/style.css`.

Built with plain HTML, CSS and a small amount of JavaScript, so it can be
hosted anywhere without a build step.
