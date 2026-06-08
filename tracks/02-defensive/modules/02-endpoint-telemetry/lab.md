# Lab 02 — Read Endpoint Telemetry From a Real Attack

## Setup
A Windows VM you own (Sysmon + the SwiftOnSecurity config) to generate your own telemetry — **or**,
fully self-contained, a real public sample:
- [EVTX-ATTACK-SAMPLES](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES) — real Sysmon/Windows
  event logs captured during actual attack techniques.
- To generate your own: [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) runs real
  ATT&CK techniques safely on your lab host.

## Scenario
Find an attacker's footprints in real endpoint telemetry — without needing to have run the attack
yourself.

> Your own VM, or the public sample logs. (If you did Track 01, ingest your *own* attack's telemetry
> instead — same skill.)

## Do
1. [ ] Get real endpoint telemetry: load an EVTX-ATTACK-SAMPLES capture, or generate events with one
   Atomic Red Team test on your VM.
2. [ ] Find the malicious process: trace its command line and its parent. (What's a normal parent
   for this process — and is this one normal?)
3. [ ] Identify the Sysmon Event IDs that captured the activity.
4. [ ] Note what a detection for this would key on.

## Success criteria — you're done when
- [ ] You found the malicious process and its ancestry in real telemetry.
- [ ] You can name the Sysmon Event IDs involved.
- [ ] You can describe what a detection would match on.

## Deliverables
`endpoint-telemetry.md`: the malicious event, its process ancestry, the Event IDs, and your
detection idea.

## AI acceleration
Have a model explain an unfamiliar command line or Event ID — then confirm against the process tree
and the real data before calling it malicious.

## Connects forward
These events and detection ideas feed module 08 (detection-as-code) and module 11 (endpoint
hunting).

## Marketable proof
> "I deploy Sysmon and read endpoint telemetry from real attack samples — process ancestry, command
> lines, Event IDs — to find malicious activity."

## Automate & own it
**Required.** Write a script (PowerShell or Python) that pulls the relevant Event IDs from an EVTX
and flags suspicious process ancestry; AI drafts, you review it against the real sample; commit it.

## Stretch
- Run an Atomic Red Team test, capture your *own* Sysmon telemetry, and find it — closing the
  attacker→defender loop yourself.
