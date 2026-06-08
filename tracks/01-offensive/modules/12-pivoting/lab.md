# Lab 12 — Pivot Into an Internal Network

## Setup
Docker-first — a multi-host lab: a reachable "DMZ" host on a network you can touch, and an
"internal" host reachable *only* through it. (A docker-compose with two networks, where one
container bridges both, models this; or use a TryHackMe/HTB pivoting room.)

## Scenario
From a foothold on the DMZ host, reach and interact with an internal host you cannot reach
directly.

> Your own lab / authorised practice ranges only.

## Do
1. [ ] Map the foothold's network position: what interfaces and routes does it have? What
   internal range can it reach that you can't?
2. [ ] Stand up a tunnel through the foothold (ligolo-ng or chisel) so your machine can route
   into the internal network.
3. [ ] Reach a service on the internal host through the tunnel — prove the pivot works.
4. [ ] Move laterally: use credentials or an exploit to gain access to the internal host.

## Success criteria — you're done when
- [ ] You reached an internal-only host from your own machine through the foothold.
- [ ] You can draw the network and explain each hop of your tunnel.
- [ ] You gained access to the second host and can name the lateral-movement technique.

## Deliverables
`pivoting.md`: the network diagram, the tunnel setup, and how you reached and accessed the
internal host.

## AI acceleration
Have a model sanity-check your routing/tunnel plan — then verify the subnets and routes
yourself. A wrong route can sever your foothold.

## Connects forward
Lateral movement is the heart of Track 06 (Active Directory); the defensive inverse is
segmentation (Track 11, ZTNA) and detection (Track 02).

## Marketable proof
> "I pivot through a compromised host into a segmented internal network and move laterally —
> and can explain the segmentation and detection that stop it."

## Automate & own it
**Required.** Script your pivot setup (tunnel + proxychains config + the route commands) so
it's repeatable from notes; AI drafts it, you verify the routes; commit it.

## Stretch
- Build a *double* pivot through two segments, and explain why each layer of segmentation
  raises the attacker's cost.
