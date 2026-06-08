# Plaintext — Lab Validation Backlog & Session Prompt

> **How to use this:** paste the "Session prompt" block below into a fresh Claude / Claude Code
> session (mobile or desktop) to continue the work. The checklist further down is the live tracker —
> tick a box when a lab is built **and** validated. Keep this file updated as the source of truth for
> "what's left."

---

## Session prompt (paste this)

You are continuing work on **Plaintext**, an open security-education curriculum (the "SANS, but free"
project). Two repos, both in the `plaintext-security` GitHub org and cloned side-by-side locally:

- `plaintext/` — the curriculum **prose** (Markdown under `tracks/`), published via Material for MkDocs.
- `plaintext-labs/` — the **runnable** labs (Docker, seed data, harnesses), laid out `<track>/<NN-module>/`.

**Read first, every session:** `plaintext/CLAUDE.md` and `plaintext/CONTRIBUTING.md` — they are the
charter (the hybrid module model, the lab-target rule, and the definition of done). Follow them exactly.

**Your job:** backfill **validated lab environments** for existing modules. A module is NOT done until
its lab is built in `plaintext-labs` (a custom build or a wrapped known image) AND you have actually run
`make up` / `make demo` and seen it work. A `lab.md` that only references an external target or an
untested `docker run` line is a stub — that is the gap we are closing.

**Per-lab recipe (one lab at a time):**
1. Read the module's `plaintext/tracks/<track>/modules/<NN-module>/{README.md,lab.md}` for intent.
2. Pick the target per the charter's lab-target rule, in order: **wrap a known vulnerable image**
   (Vulhub / Juice Shop / DVWA / CloudGoat — prefer this) → **point at an external target** (PortSwigger,
   flaws.cloud) only if hosting adds nothing → **build a custom minimal target** only if it teaches the
   mechanism better. Real CVEs/datasets beat invented ones.
3. Build `plaintext-labs/<track>/<NN-module>/` with: `docker-compose.yml`, a `Makefile`
   (`up`/`down`/`reset`/`demo`[/`shell`]), small **committed** seed data in `data/`, and any
   Dockerfile/harness. Pin image tags and tool versions.
4. **Validate:** `make up && make demo && make down` — actually run it, debug until it works. A demo
   should deterministically show the lesson and exit cleanly.
5. Repoint `plaintext/tracks/.../<NN-module>/lab.md` Setup to `git clone … && cd <track>/<module> &&
   make up`; keep the real production tool as the learner's build target where relevant.
6. Verify prose still builds: in `plaintext/`, `mkdocs build --strict` (use the local `.venv`).
7. Commit: push the lab to `plaintext-labs` (`main`); commit the `lab.md` repoint to `plaintext` on a
   track branch (`feat/<track>-labs`) and open a PR. Never commit secrets or heavy artifacts
   (`*.pcap`, dumps, keys) — `.gitignore` covers them; only small curated seed data is committed.

**Guardrails:** OSS-first; every offensive lab keeps the authorization note (own/authorised targets,
intentionally-vulnerable only); ground labs in the fictional **Meridian Financial** estate where it
fits; don't claim a lab works unless you ran it.

**Work the checklist below in order (defensive → offensive → foundations). Tick each box only after
`make demo` passed. Then report which labs you completed and what's next.**

---

## Status (as of this handoff)

- **Prose:** all 43 existing modules have the `## The core idea` bridge (foundations 12, offensive 16,
  defensive 15). Merged to `main` (PRs #4, #6, #7, #8).
- **Labs built & validated: 43 / 43** — all 12 foundations + all 16 offensive + all 15 defensive labs
  validated with `make demo`. Open PRs: #11 (offensive), #10 (defensive), #12 (foundations).
- **Empty stub tracks (no modules yet):** 03-forensics, 04-malware, 05-cloud, 06-active-directory,
  07-endpoint-hardening, 08-cryptography, 09-python-for-security, 10-automation, 11-ztna,
  12-ai-augmented-ops — these need modules **authored from scratch** (prose + labs together), a separate
  larger effort to plan track-by-track.

---

## Lab backfill checklist (build + validate)

### Defensive (`02-defensive`) — 15/15 done
- [x] 07-log-parsing — *stdlib parse-rate harness over a messy sshd sample*
- [x] 08-detection-as-code — *sigma-cli + teaching matcher*
- [x] 01-telemetry — *SSH log pipeline demo → structured records + analyst gaps*
- [x] 02-endpoint-telemetry — *Sysmon event analysis + attack chain reconstruction*
- [x] 03-linux-telemetry — *osquery querying the container; auditd rules demo*
- [x] 04-network-monitoring — *Zeek log analysis: beaconing, DGA, C2 domain*
- [x] 05-intrusion-detection — *Suricata alert analysis over bundled eve.json*
- [x] 06-siem — *multi-source correlation harness; 6 alerts across 5 rules*
- [x] 09-detection-testing — *purple-team detection loop: 3/3 atomics fire, 0 FP*
- [x] 10-attack-coverage — *ATT&CK Navigator layer from Sigma rule set + gap report*
- [x] 11-hunting-endpoint — *SQL-based Sysmon hunt: hypothesis confirmed*
- [x] 12-hunting-network — *RITA-style beacon hunt: score 87/100 top candidate*
- [x] 13-triage-ir — *NIST SP 800-61 5-phase guided IR triage harness*
- [x] 14-threat-intel — *indicator enrichment: 3 IOCs enriched, 1 clean*
- [x] 15-soar — *four-stage SOAR playbook: 2 escalated, 1 suppressed*

### Offensive (`01-offensive`) — 16/16 done
- [x] 06-web-injection — *custom vulnerable Flask app; UNION-extract demo*
- [x] 01-recon — *passive recon harness over a target you own; script the asset inventory*
- [x] 02-scanning — *nmap three-phase scan (scanner + victim compose)*
- [x] 03-vuln-id — *CVE→CWE→CVSS→KEV→PoC research harness*
- [x] 04-exploitation — *CVE-2021-41773 Apache path traversal + RCE (Vulhub)*
- [x] 05-memory-corruption — *stack buffer overflow ret2win; dynamic offset discovery*
- [x] 07-web-access-control — *IDOR + vertical escalation via X-Role header*
- [x] 08-web-ssrf-xxe — *SSRF to mock metadata endpoint + XXE file read*
- [x] 09-password-attacks — *MD5/NTLM/bcrypt cracking; 8/11 cracked, bcrypt stood firm*
- [x] 10-privesc-linux — *SUID find + sudo NOPASSWD + writable cron; all three paths*
- [x] 11-privesc-windows — *triage.py parsing winPEAS text output; P0-P3 scoring*
- [x] 12-pivoting — *DMZ→internal TCP relay; attacker genuinely can't skip the pivot*
- [x] 13-c2-postex — *custom Flask C2: beacon/task/result channel; 4 post-ex commands*
- [x] 14-lolbins-evasion — *download/exec/persist via native binaries only*
- [x] 15-cloud-primer — *flaws.cloud external validated; CloudGoat + Pacu quick ref*
- [x] 16-reporting — *validate.py 11/11 structural checks; public report refs verified*

### Foundations (`00-foundations`) — 12/12 done
- [x] 01-security-principles — *breach analysis guide + CISA KEV sampler (no Docker)*
- [x] 02-lab-setup — *Docker/git check + VM isolation guide + snapshot workflow*
- [x] 03-docker — *container lifecycle demo: root-by-default + fixed Dockerfile*
- [x] 04-linux — *Ubuntu container with planted users; triage: users/SUID/ps/log analysis*
- [x] 05-windows — *EVTX-shaped sample + PowerShell collect script (no Docker)*
- [x] 06-networking — *netshoot compose; live DNS+HTTP demo + annotated capture*
- [x] 07-web-http — *Flask echo server; GET/POST/redirect/cookie/IDOR header demo*
- [x] 08-data-encoding — *base64 PS decode, hex C2 domain, URL traversal, KEV jq*
- [x] 09-cryptography — *SHA-256, AES round-trip, RSA, cert read, AES bit-flip*
- [x] 10-scripting — *topips.py scaffold + reference impl; edge cases explained*
- [x] 11-version-control — *git check + .gitignore + gitleaks guide (no Docker)*
- [x] 12-threat-modeling — *STRIDE template + threat-model.md validator (no Docker)*

> For the "design/paper" modules, "validated" means the exercise is concrete and doable as written —
> not a forced container. Say so in `lab.md` rather than inventing a hollow environment.

---

## Other backlog (not lab-validation)

- [ ] **Link-validation sweep** — every `Learn`/Further-reading link across the 43 modules must resolve
  to the specific, current resource (no invented YouTube IDs). Not yet done.
- [ ] **README track table is stale** — lists 6 tracks; 12 exist. Fix it.
- [ ] **Author the 9 stub tracks** from scratch (prose + labs together), track-by-track, full modules.
  Likely order: cloud / forensics / malware first (flagship-adjacent).
