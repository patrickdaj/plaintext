# Track 07 — Endpoint & Host Hardening

**Make the host expensive to attack and loud when attacked.** Harden Windows and Linux to
recognised benchmarks — as code, with compliance scoring and drift detection.

## What you'll be able to do
- Threat-model the endpoint and prioritise what actually matters.
- Harden Windows and Linux to CIS benchmarks, expressed as code.
- Score compliance and detect configuration drift.
- Stand up endpoint telemetry that catches what hardening doesn't stop.

## Modules

| # | Module | What you'll learn | OSS tools |
|---|--------|-------------------|-----------|
| 01 | Threat Model of the Endpoint | What you're defending and from what | — |
| 02 | Windows Hardening to CIS | Baseline configuration that holds up | `LGPO`, CIS-CAT-lite |
| 03 | Linux Hardening to CIS | Securing the Linux host as a baseline | `OpenSCAP`, `Lynis` |
| 04 | Exploit Mitigation & Allowlisting | ASLR/DEP, app control, attack-surface reduction | `AppLocker`, `fapolicyd` |
| 05 | Endpoint Telemetry & EDR | Visibility into process/file/auth events | `osquery`, `wazuh` |
| 06 | Configuration Management | Hardening at scale, as code | `ansible` |
| 07 | Compliance Scoring & Auditing | Measuring posture against a benchmark | `OpenSCAP` |
| 08 | Patch & Vulnerability Management | Finding and closing exposure | `osquery`, `grype` |
| 09 | Local Privilege-Escalation Defense | Closing the paths Track 01 abuses | — |
| 10 | Detecting Host Compromise | Catching what the baseline didn't stop | `wazuh`, `sigma` |

## Prerequisites
Complete Track 00 — Foundations first.

> Work on VMs or containers you own. Some hardening is destructive — snapshot first.

## Capstone
Harden a Windows and a Linux host to CIS as code, score the before/after compliance, prove
drift detection catches a deliberate misconfiguration, and show telemetry firing on a
simulated attack. **Deliverable:** the config-as-code, the score delta, and the detection.

## AI & automation
AI generates the hardening (Ansible, GPO, SCAP profiles) — and that's exactly where silent
mistakes hide. The skill is reviewing generated configuration against the benchmark and
your threat model before it ships. AI authors the baseline; you own what it breaks.

## Standards & further reading
- CIS Benchmarks (Windows, Linux) and the CIS Controls
- NIST SP 800-123 (Server Security) and SP 800-128 (Config Management)
- DISA STIGs as an alternate baseline
