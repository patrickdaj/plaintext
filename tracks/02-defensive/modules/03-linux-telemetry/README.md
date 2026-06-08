# Module 03 — Linux Telemetry

**Defensive Operations** — *servers and containers are Linux; this is how you watch them.*

## Why this matters
Cloud workloads, web servers, and containers run Linux, where default logging tells you little
about *what executed*. auditd and osquery turn a Linux host into a queryable sensor — process
execution, file access, network connections — the visibility the cloud and detection tracks assume.
Without it, a compromised Linux host is a blind spot.

## Objective
Configure Linux audit logging, query host state with osquery, and capture the execution telemetry
detections rely on.

## Learn (~4 hrs)

**The Linux sensor**
- [osquery documentation](https://osquery.readthedocs.io/) — query your host like a database; read "Getting Started" and a few example queries.
- [Linux Audit (auditd) documentation](https://github.com/linux-audit/audit-documentation/wiki) — the kernel audit framework: rules, events, and what to log.

**What to log**
- [MITRE ATT&CK — Data Source: Process](https://attack.mitre.org/datasources/DS0009/) — collect with detection in mind (same lens as the Windows module, Linux side).

## Key concepts
- auditd: rules, syscalls, and the event format
- osquery: host-as-a-database for live and scheduled queries
- Process execution + file + network telemetry on Linux
- eBPF-based tooling (the modern direction)
- Containers: where host telemetry sees — and misses — container activity

## AI acceleration
A model writes auditd rules and osquery SQL quickly — but an over-broad audit rule floods you with
noise and a wrong osquery join misses the event entirely. Test what the rule actually captures
against real activity.
