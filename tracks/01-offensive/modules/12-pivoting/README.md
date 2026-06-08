# Module 12 — Pivoting & Lateral Movement

**Offensive Security** — *one foothold is rarely the goal; this is how access spreads through a network.*

## Why this matters
Real targets are segmented: the host you compromise can usually reach internal systems you
can't touch directly. Pivoting — routing your traffic *through* a foothold — and lateral
movement are how a single foothold becomes domain-wide compromise, and they're exactly what
defenders segment and hunt against. Understanding the attacker's tunnel is also how you argue
for network segmentation.

## Objective
Pivot through a compromised host to reach an internal network you can't reach directly, and
move laterally to a second target in your lab.

## Learn (~4 hrs)

**Tunneling & pivoting**
- [Pivoting Made Easy with Ligolo-ng (video)](https://www.youtube.com/watch?v=txFnX5NPqKc) — the modern, clean way to tunnel into an internal network.
- [Ligolo-ng (project + README)](https://github.com/nicocha30/ligolo-ng) and [Chisel](https://github.com/jpillora/chisel) — the two tools you'll reach for; read their usage.

**Where it sits**
- [MITRE ATT&CK — Lateral Movement (TA0008)](https://attack.mitre.org/tactics/TA0008/) — the techniques and how they're detected.

## Key concepts
- Network segmentation and why a foothold matters
- Port forwarding vs SOCKS proxying vs a tunnel interface
- Pivoting tools (ligolo-ng, chisel) and proxychains
- Lateral movement techniques (and their telemetry)
- Double pivots through multiple segments

## AI acceleration
A model explains a tunneling setup and generates the commands — but pivoting is unforgiving of
a wrong route or a misread subnet, and you can lose your foothold. Map the network yourself and
understand each hop before you build the tunnel.
