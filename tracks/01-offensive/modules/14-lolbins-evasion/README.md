# Module 14 — Living-off-the-Land & Evasion

**Offensive Security** — *the quietest attacks bring no tools — they use what's already there.*

## Why this matters
Modern defenses flag unknown binaries, so real operators "live off the land": abusing trusted,
signed, native tools (certutil, regsvr32, bitsadmin) to download, execute, and persist without
dropping anything obvious. LOLBin abuse is among the most common techniques in real intrusions
precisely because it blends into normal activity — which is exactly why understanding it
matters for both red and blue.

## Objective
Accomplish attacker tasks (download, execute, persist) using only native binaries, and
understand the telemetry that still catches them.

## Learn (~4 hrs)

**The technique**
- [Living Off The Land Attacks Explained — LOLBins (video)](https://www.youtube.com/watch?v=lDK384LXhpU) — why and how attackers abuse native tooling.
- [LOLBAS Project](https://lolbas-project.github.io/) (Windows) and [GTFOBins](https://gtfobins.github.io/) (Unix) — the canonical catalogs; you'll search these constantly.

**Where it sits**
- [MITRE ATT&CK — Defense Evasion (TA0005)](https://attack.mitre.org/tactics/TA0005/) — the tactic, and how detections catch LOLBin abuse anyway.

## Key concepts
- Why "fileless" / LOLBin techniques evade signature defenses
- Common LOLBins: download cradles, execution, persistence
- Application allow-listing bypasses
- Basic AV/EDR evasion concepts — and their limits
- Why behaviour-based detection still catches you

## AI acceleration
A model suggests LOLBin one-liners instantly — and just as easily suggests one that's heavily
signatured or that doesn't exist on the target. Verify each against LOLBAS/GTFOBins and the
target's actual binaries; evasion that isn't is just noise. (This module is dual-use — the goal
is to understand the technique so you can *detect* it; keep it in your own lab.)
