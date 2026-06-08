# Track 06 — Active Directory & Windows Security

**The enterprise runs on Active Directory, and so do most intrusions.** Learn the Windows
and AD security model by attacking it and then closing the paths as code.

## What you'll be able to do
- Enumerate an AD environment and read its attack paths.
- Execute and explain the core Kerberos and credential attacks.
- Find a path to Domain Admin and walk it.
- Detect those attacks and harden the domain as code.

## Modules

| # | Module | What you'll learn | OSS tools |
|---|--------|-------------------|-----------|
| 01 | AD & Windows Security Model | Domains, trusts, tokens, and auth | — |
| 02 | Enumeration | Mapping users, groups, and paths | `BloodHound`, `SharpHound` |
| 03 | Kerberos Attacks | Kerberoasting and AS-REP roasting | `impacket`, `Rubeus` |
| 04 | Credential Theft & Replay | Pass-the-hash / pass-the-ticket | `impacket`, `mimikatz` |
| 05 | ACL & Delegation Abuse | Object permissions and delegation paths | `BloodHound`, `PowerView` |
| 06 | Lateral Movement | Moving host to host inside the domain | `impacket`, `crackmapexec` |
| 07 | Persistence in AD | Golden/silver tickets and other footholds | `impacket` |
| 08 | Path to Domain Admin | Chaining findings to full control | `BloodHound` |
| 09 | Detecting AD Attacks | Event logs, honeytokens, and signals | `sigma`, `wazuh` |
| 10 | Hardening AD as Code | Tiering, baselines, and measuring posture | `PingCastle` |
| 11 | Defending Identity | Protecting Kerberos, GPO, and delegation | — |

## Prerequisites
Complete Track 00 — Foundations; Track 01 — Offensive helps.

> Build your own lab domain (e.g. GOAD — Game of Active Directory, or a local Windows eval
> VM). Only attack environments you own.

## Capstone
Find an attack path from a low-privilege user to Domain Admin in a lab domain, walk it,
then close it: harden as code and write detections for each step you used. **Deliverable:**
the attack path, the before/after posture score, and the detections.

## AI & automation
AI summarises BloodHound paths and drafts detection logic, but the domain is unforgiving of
hallucination — every path is validated in the lab, and generated hardening is reviewed
before it touches Group Policy. AI accelerates the analysis; you own the change.

## Standards & further reading
- MITRE ATT&CK (Enterprise) — Credential Access, Lateral Movement, Persistence
- Microsoft AD security and tiering guidance
- The BloodHound and Impacket documentation
