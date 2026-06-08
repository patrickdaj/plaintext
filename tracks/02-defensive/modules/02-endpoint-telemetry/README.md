# Module 02 — Windows & Endpoint Telemetry

**Defensive Operations** — *the endpoint sees what the network can't; Sysmon is how you make it talk.*

## Why this matters
Most attacker activity — process creation, injection, persistence — happens on the endpoint, where
default Windows logging is thin. Sysmon turns a Windows host into a rich detection sensor, and its
event schema underlies a huge share of real-world detections. Learning what to collect and read
here is what makes the later detection and hunting modules possible.

## Objective
Deploy Sysmon with a good config, and read the process/network/persistence events that real
detections are built on — using real attack telemetry.

## Learn (~4 hrs)

**The endpoint sensor**
- [What is Sysmon — How to Install and Set Up Sysmon (video)](https://www.youtube.com/watch?v=PY1v_mZnjks) — install and configure the endpoint sensor.
- [SwiftOnSecurity sysmon-config](https://github.com/SwiftOnSecurity/sysmon-config) — the community baseline config; read it to learn what's worth collecting and why.

**Reading the events**
- [MITRE ATT&CK — Data Source: Process](https://attack.mitre.org/datasources/DS0009/) — how Sysmon events map to techniques.

## Key concepts
- Why default Windows logging isn't enough
- Key Sysmon Event IDs (1 process-create, 3 network, 11 file, 13 registry)
- Process ancestry and command-line logging
- Endpoint agents (Sysmon → Wazuh / EDR)
- Tuning: signal vs volume

## AI acceleration
A model explains a Sysmon Event ID or a suspicious command line instantly — a genuine accelerator
when triaging. But it'll also rationalise a benign-looking event that's actually malicious (or
vice-versa); confirm against the process ancestry and the real data, not the model's vibe.
