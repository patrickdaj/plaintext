# Module 04 — Network Security Monitoring

**Defensive Operations** — *the network doesn't lie; Zeek turns packets into evidence.*

## Why this matters
Endpoints can be blinded, but traffic still crosses the wire. Network Security Monitoring with Zeek
turns raw packets into rich, structured protocol logs — connections, DNS, HTTP, TLS, files — that
reveal C2, exfiltration, and lateral movement an endpoint might miss. It's a cornerstone of real SOC
visibility, and you can practice it on real malicious traffic for free.

## Objective
Run Zeek over real network traffic and read its logs to find malicious activity.

## Learn (~4 hrs)

**The NSM tool**
- [A Technical Introduction to Zeek/Bro (video)](https://www.youtube.com/watch?v=R-8WdoP-CtE) — what Zeek is and why its logs beat raw packets.
- [Zeek documentation](https://docs.zeek.org/) — read "Getting Started" and the logs reference (conn, dns, http, ssl).

**Read real traffic**
- [Malware-Traffic-Analysis.net](https://www.malware-traffic-analysis.net/) — free, real malicious PCAPs with write-ups; your self-contained dataset.

## Key concepts
- Packets → protocol logs (conn, dns, http, ssl, files)
- What NSM catches that endpoints miss (C2, exfil, lateral movement)
- Zeek scripting and signatures (high level)
- Indicators in network logs (JA3, suspicious DNS, beaconing)
- Full-packet capture vs metadata (Arkime)

## AI acceleration
A model summarises a Zeek `conn.log` or explains a suspicious DNS pattern fast — useful triage. But
it can't see your network's baseline, so it'll flag normal-for-you traffic or miss a subtle beacon.
Confirm against the logs and the known-bad write-up.
