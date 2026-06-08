# Contributing to Plaintext

Thanks for helping make security education free and open.

## How to contribute

1. Fork the repo
2. Create a branch: `git checkout -b feat/your-module-name`
3. Add your content following the structure and templates below
4. Preview it locally (see below), then submit a pull request

New modules can also be proposed first via the **New Module** issue template
(`.github/ISSUE_TEMPLATE/new-module.md`) — it captures everything a module needs.

## Preview locally

The site is built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
from the Markdown under `tracks/`:

```bash
python3 -m pip install -r requirements.txt
mkdocs serve            # live preview at http://127.0.0.1:8000
mkdocs build --strict   # what CI runs — fails on broken links or pages missing from nav
```

When you add a module, also add its pages to the `nav:` tree in `mkdocs.yml`
(`--strict` fails on any page that is not in the nav).

## Module structure

Each module lives at `tracks/<track>/modules/<NN>-<name>/` and contains:

- `README.md` — concept explanation (your own original writing)
- `lab.md` — a hands-on, Docker-first exercise

Each **track** (`tracks/<NN>-<name>/README.md`) is a content map that ends in a
**capstone** — a portfolio-worthy artifact that proves the track.

## Content rules

- **Write everything in your own words from primary sources.** No copying from SANS,
  Offensive Security, or other proprietary course material. Topic coverage may be
  informed by such courses; the prose must be original.
- **Open-source first, not open-source only.** Prefer OSS tools; free/community editions
  and the genuine real-world tool are fine where that is what the job uses. Labs must
  stay reproducible at zero cost.
- **Hands-on and job-ready** — "in the dirt," not certification theory. Every module ends
  in something the learner *does*.
- **Docker-first labs.** Default to containers; use VMs or cloud free-tier accounts only
  where the domain demands it (Active Directory, cloud).
- **AI woven through.** Show the AI-acceleration move for the topic, and the judgment that
  goes with it: *AI authors → you review → you own it*.
- **Cite multiple primary sources** (CVEs, RFCs, tool docs, research papers, MITRE ATT&CK).
- **Keep lab artifacts out of commits** — packet captures, keys, dumps, and logs are
  referenced in the prose, never checked in (see `.gitignore`).

## Module README template

```markdown
# Module Title

## Objective
What the learner will be able to do after this module (job-relevant, one sentence).

## Background
Core concept explanation, written originally from primary sources.

## Key concepts
- Concept 1
- Concept 2

## AI acceleration
The specific way AI/automation speeds this up — and what you must review and own.

## Further reading
- Multiple primary sources: RFC / CVE / OSS docs / ATT&CK / paper
```

## Lab template

```markdown
# Lab: Title

## Setup
Docker-first: the container(s) / image(s) to run, and how. (VM or cloud free-tier only
if the domain requires it.) Keep it reproducible at zero cost.

## Scenario
What you're trying to do and why — against an intentionally vulnerable target.

> Only test systems you own or have explicit written permission to test.

## Steps
1. Step one
2. Step two

## Expected output
What success looks like. (Reference any captures/artifacts — do not commit them.)

## AI acceleration
Where a model helps (triage, generation, summarising) and what you verify by hand.

## Questions
1. What did you observe?
2. How would you detect or defend against this?
```
