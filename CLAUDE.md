# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Plaintext is an open security-education curriculum (CC BY 4.0). It is a **content repository plus a static landing page** — there is no application code, build system, package manager, or test suite. Work here is almost entirely Markdown authoring and editing one hand-written HTML page.

## Repo map

```
plaintext/
├── docs/                  # the published site — the ONLY directory GitHub Pages serves
│   ├── index.html             # the landing page (standalone, CSS inlined)
│   └── tracks/                # GENERATED curriculum-map pages — do not hand-edit
│       ├── track.css             # shared styling for the map pages
│       └── <NN-track-name>.html  # rendered from tracks/<NN>/README.md
├── tracks/                # the Markdown curriculum — the SOURCE OF TRUTH for content
│   └── <NN-track-name>/
│       ├── README.md          # track overview (intro + module table) → rendered to docs/tracks/
│       └── modules/<NN-module-name>/
│           ├── README.md      # concept explanation
│           └── lab.md          # hands-on OSS-only exercise
├── tools/build_track_pages.py # regenerates docs/tracks/*.html from tracks/*/README.md
├── CONTRIBUTING.md        # canonical module/lab templates + content rules — read before authoring
├── README.md              # repo intro + track table
├── LICENSE                # CC BY 4.0
└── .github/
    ├── workflows/deploy.yml         # GitHub Pages deploy (push to main → publishes docs/)
    └── ISSUE_TEMPLATE/new-module.md # how new modules are proposed
```

## The site, the curriculum, and how they connect

Two layers, with a one-way generator bridging them:

1. **`docs/index.html`** — the hand-authored landing page. Standalone, all CSS inlined in a `<style>` block (no framework, no external assets except a Google Fonts link). Its track cards link to the generated map pages under `docs/tracks/`.
2. **`tracks/`** — the curriculum, authored in Markdown. **This is the source of truth for all curriculum content.**
3. **`docs/tracks/<NN>.html`** — published map pages, **generated** from each `tracks/<NN>/README.md` by `tools/build_track_pages.py`. They share `docs/tracks/track.css`.

The critical rule:
- **Never hand-edit `docs/tracks/*.html`.** Edit the track `README.md` under `tracks/`, then re-run `python3 tools/build_track_pages.py` to regenerate. Hand edits will be overwritten and the two will silently drift.
- `index.html` is still hand-authored — it is *not* generated. Only the per-track map pages are.
- Only `docs/` is published (see Deployment). The `tracks/` Markdown and `tools/` script are in the repo but **not** served; the live curriculum pages are the rendered copies under `docs/tracks/`.
- The generator only renders track-level `README.md` files. Module `README.md`/`lab.md` content is **not** yet rendered to the site — if a task implies it should be, that wiring does not exist yet; flag it.

## Deployment

`.github/workflows/deploy.yml` deploys to GitHub Pages via GitHub Actions, **on push to `main` only**. It uploads `./docs` as the Pages artifact — so only files inside `docs/` are published. The site is a project page served under the `/plaintext/` path (`https://patrickdaj.github.io/plaintext/`); keep that in mind for any absolute paths.

Deployment itself stays build-free: Pages serves the committed `docs/` as-is. The one generation step is **local and optional** — `tools/build_track_pages.py` (stdlib-only Python 3, no dependencies) renders the track maps into `docs/tracks/`. Run it after editing any track `README.md`, then commit the regenerated HTML alongside the Markdown so the published pages stay in sync. CI does not run it.

To preview the site locally, open `docs/index.html` in a browser, or serve it with `python3 -m http.server` from the `docs/` directory. (The published Pages site may be unreachable from sandboxed environments that block `*.github.io`; verify a deploy succeeded via the GitHub Actions run status instead.)

## Content structure and authoring rules

Track and module directories are zero-padded and numbered (`00-foundations`, `modules/01-networking`); see the [Repo map](#repo-map) for the layout. The canonical templates for a module `README.md` and `lab.md`, plus the curriculum content rules, live in `CONTRIBUTING.md` — follow them when adding or editing modules. Key non-obvious rules from there:

- All prose must be **original writing from primary sources**. Do not copy from SANS, Offensive Security, or other proprietary course material.
- Reference and use **open source tools only**; labs must be reproducible with free tools.
- Cite sources (CVEs, RFCs, tool docs, papers) in "Further reading".
- Labs are **offensive-capable by nature** — keep the standing authorization rule explicit in any lab that attacks a target: only test systems you own or have explicit written permission to test, and point learners at intentionally vulnerable targets (DVWA, locally spun VMs, free CTF rooms).

New modules are proposed via the `.github/ISSUE_TEMPLATE/new-module.md` issue template.

## Secret & artifact hygiene

This repo has **no `.gitignore`**, yet the labs drive tools (tcpdump, openssl, metasploit, volatility, prowler, …) that emit exactly the kind of files you must never commit: packet captures (`*.pcap`), keys and credentials (`*.pem`, `*.key`, `*_rsa`), tokens, and verbose logs. When a lab generates artifacts, keep them out of commits — reference them in the lab text rather than checking them in, or add a scoped `.gitignore` for that work. Never commit real secrets or capture data into curriculum content.
