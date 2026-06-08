# Lab 13 — Run an Open-Source C2

## Setup
Docker-first — a [Sliver](https://github.com/BishopFox/sliver) server, and a lab host to
implant (a container or VM you own).

## Scenario
Get a managed C2 session on a host in your lab and perform basic post-exploitation, watching
what you generate on the wire.

> Your own lab only.

## Do
1. [ ] Stand up the Sliver server and a listener.
2. [ ] Generate an implant, deliver it to your lab host, and catch the session.
3. [ ] Post-ex: enumerate the host, collect something of interest, and establish a simple
   persistence.
4. [ ] Switch hats: capture the C2 traffic (Foundations networking) and note the beaconing
   artifacts a defender would see.

## Success criteria — you're done when
- [ ] You have a working C2 session and ran post-ex through it.
- [ ] You established persistence and can explain it.
- [ ] You can name two artifacts your C2 left for a defender (host or network).

## Deliverables
`c2-postex.md`: the session setup, the post-ex you ran, the persistence, and the
defender-visible artifacts.

## AI acceleration
Use a model to draft post-ex enumeration commands — then judge which are worth the noise before
running them. The model lists options; you choose what's safe to do.

## Connects forward
The artifacts you generate here are exactly what Track 02 (detection) and Track 03 (forensics)
hunt; persistence ties to Track 06.

## Marketable proof
> "I run an open-source C2 end to end — implant, session, post-exploitation, persistence — and
> can articulate the telemetry it leaves for defenders."

## Automate & own it
**Required.** Script your implant generation and listener setup so an engagement is
reproducible; AI drafts it, you review; commit it (no live implants in the repo).

## Stretch
- Tune the implant's beacon interval and jitter, and explain how that changes the detection
  picture.
