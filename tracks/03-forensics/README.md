# Track 03 — Digital Forensics & Incident Response

**Reconstruct events from the artifacts left behind** and tell the story of what happened
on a system — defensibly, so the timeline holds up. Acquisition through root-cause report.

## What you'll be able to do
- Acquire and verify evidence without altering it.
- Recover and interpret artifacts from disk, memory, and the network.
- Build a super-timeline that correlates activity across sources.
- Drive an investigation to a root-cause verdict and write it up.

## Modules

| # | Module | What you'll learn | OSS tools |
|---|--------|-------------------|-----------|
| 01 | Forensic Fundamentals & Evidence Handling | Integrity, hashing, chain of custody | `dc3dd`, `sleuthkit` |
| 02 | Acquisition & Imaging | Capturing disk and memory soundly | `dc3dd`, `avml` |
| 03 | File Systems & Carving | NTFS/ext internals; recovering deleted data | `sleuthkit`, `foremost` |
| 04 | Windows Artifacts | Registry, event logs, prefetch, execution | `RegRipper`, `EZ tools` |
| 05 | Browser & Application Artifacts | User activity and app traces | `autopsy`, `hindsight` |
| 06 | Memory Forensics | Processes, injection, connections from RAM | `volatility3`, `MemProcFS` |
| 07 | Timeline Analysis | Building and pivoting a super-timeline | `plaso`, `timesketch` |
| 08 | Triage & Live Response | Scaling collection across hosts | `velociraptor` |
| 09 | Network Forensics | Reconstructing sessions and files from PCAP | `wireshark`, `zeek` |
| 10 | Log & Cloud Forensics | Investigating from logs and cloud trails | `hayabusa`, `chainsaw` |
| 11 | Anti-Forensics & Detecting It | Timestomping, wiping, and spotting them | `sleuthkit` |
| 12 | Malware Artifacts in IR | Handing off to deep analysis (→ T04) | `capa`, `yara` |
| 13 | Incident Response Process | The NIST lifecycle in practice | — |
| 14 | Reporting & Root-Cause Analysis | A report that survives scrutiny | — |

## Prerequisites
Complete Track 00 — Foundations first.

> Labs use public training images and sample memory dumps. Never examine evidence you're
> not authorised to handle.

## Capstone
Take a training disk or memory image to a root-cause incident report: acquire and verify,
build a super-timeline, and reconstruct what happened — every claim tied to an artifact.
**Deliverable:** the timeline and a report that would survive scrutiny.

## AI & automation
AI summarises timelines, correlates artifacts, and drafts the incident narrative far faster
than you can by hand. Forensic soundness sets the limit: an AI summary is a *lead*, never
evidence — every conclusion traces back to the artifact. Automate collection and parsing;
never automate the judgment about what happened.

## Standards & further reading
- NIST SP 800-86 (Forensic Techniques into Incident Response)
- NIST SP 800-61 (Incident Handling Guide)
- SWGDE best practices for digital evidence
- Volatility and Sleuth Kit documentation
