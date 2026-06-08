# Module 16 — Reporting & Remediation

**Offensive Security** — *the report is the product; a shell nobody can act on is worthless.*

## Why this matters
Clients and defenders don't buy shells — they buy a clear, prioritised, reproducible account of
what's wrong and how to fix it. Reporting is the single most career-defining offensive skill: it
separates a "tool runner" from a professional, and it's the deliverable that gets you hired and
re-hired. This module turns everything you found across the track into a report a defender can
act on.

## Objective
Write a professional penetration-test report — executive summary, technical findings with risk
ratings and evidence, and prioritised remediation — modeled on real public reports.

## Learn (~4 hrs)

**The standard & real examples**
- [PTES — Reporting](http://www.pentest-standard.org/index.php/Reporting) — the structure a professional report follows.
- [Public Pentesting Reports (curated collection)](https://github.com/juliocesarfort/public-pentesting-reports) — read two or three *real* reports from reputable firms to model tone, structure, and risk framing.

**Tooling**
- [Ghostwriter (GhostManager)](https://github.com/GhostManager/Ghostwriter) — open-source reporting / engagement management; optional, but see how teams operationalise it.

## Key concepts
- Audience: executive summary vs technical detail
- Findings: clear title, evidence, reproduction, impact, risk rating (CVSS + business context)
- Prioritisation by real risk (callback to KEV/EPSS, module 03)
- Actionable remediation a defender can actually implement
- Reproducibility — a finding that can't be reproduced isn't one

## AI acceleration
This is where AI shines *and* where it's most dangerous: a model drafts clean report prose from
your notes in seconds — but it will also smooth over a finding you can't reproduce or invent an
impact. AI authors the prose; you verify every finding, number, and CVE. You sign it; you own it.
