# Module 15 — Cloud & Container Attack Primer

**Offensive Security** — *where your on-prem skills meet the cloud — the bridge to Track 05.*

## Why this matters
Attacks increasingly end in the cloud: a web SSRF reaches a metadata endpoint, leaked keys
unlock a storage bucket, a container escape lands on the node. This primer connects the
offensive skills you've built to cloud-native targets — IAM, metadata, storage, and containers
— and hands off to the full Cloud track. It's also where the Capital One SSRF you met in module
08 actually pays off.

## Objective
Exploit common cloud and container misconfigurations against a deliberately vulnerable
environment, and explain the path from a web/host foothold to cloud compromise.

## Learn (~4 hrs)

**Hands-on, real targets**
- [flaws.cloud](http://flaws.cloud/) — a free, guided, real-world AWS pentest you do in the browser; the best on-ramp to cloud attacking.
- [CloudGoat (Rhino Security Labs)](https://github.com/RhinoSecurityLabs/cloudgoat) — deliberately vulnerable AWS scenarios you deploy and attack with [Pacu](https://github.com/RhinoSecurityLabs/pacu).

**Where it sits**
- [MITRE ATT&CK — Cloud Matrix](https://attack.mitre.org/matrices/enterprise/cloud/) — cloud techniques and tactics.

## Key concepts
- The metadata endpoint (`169.254.169.254`) and SSRF-to-credentials
- IAM keys, roles, and privilege escalation
- Object-storage (S3) misconfigurations
- Container escape to the host/node
- Where attacker skills hand off to the Cloud track (T05)

## AI acceleration
A model explains AWS error messages and IAM policy quirks well — genuinely useful in unfamiliar
cloud terrain. But it will also hallucinate a service behaviour or an API; verify against the
provider docs, and never run cloud changes you don't understand against a live account.
