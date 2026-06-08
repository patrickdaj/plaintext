# Module 13 — Command & Control and Post-Exploitation

**Offensive Security** — *what a real operator does after the shell: persist, collect, and control — quietly.*

## Why this matters
A raw shell is fragile and loud. Real operations run over a command-and-control (C2) framework
that gives reliable, encrypted, resilient control — and post-exploitation is the tradecraft of
doing useful work without getting caught. Open-source C2 like Sliver is used by real red teams
*and* real threat actors, so understanding it is essential for both attacking and detecting.

## Objective
Stand up an open-source C2, get a managed session on a lab host, and perform post-exploitation
(enumeration, persistence) while understanding the telemetry it generates.

## Learn (~4 hrs)

**The framework**
- [Sliver C2 — Complete Guide from Installation to Post-Exploitation (video)](https://www.youtube.com/watch?v=i_rPATPFi4M) — a full walk through the modern OSS C2.
- [Sliver Wiki](https://github.com/BishopFox/sliver/wiki) — the official reference for implants, listeners, and commands.

**Where it sits**
- [MITRE ATT&CK — Command and Control (TA0011)](https://attack.mitre.org/tactics/TA0011/) — C2 techniques and how defenders detect beaconing.

## Key concepts
- Why C2 beats a raw shell (resilience, encryption, sessions)
- Implants, listeners, and beaconing
- Post-exploitation: enumeration, collection, persistence
- C2 detection (beacon timing, JA3, network artifacts) — the defender's view
- Operating quietly vs the noise you actually make

## AI acceleration
A model accelerates building post-ex commands and parsing collected data — but C2 tradecraft is
largely about *what not to do* (noisy commands that burn your access), which the model won't
weigh. You own the operational judgment.
