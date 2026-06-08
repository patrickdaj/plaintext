# Lab 14 — Live Off the Land

## Setup
A Windows VM (for LOLBAS) and/or a Linux container (for GTFOBins) you own — ideally with some
logging (Sysmon, or the real-EVTX habit from Foundations module 05) so you can see your own
tracks.

## Scenario
Accomplish a task — download and execute a payload, then persist — using only native, trusted
binaries, then look at what you left behind.

> Your own lab only.

## Do
1. [ ] Using only native binaries, build a "download cradle" that fetches a file from your own
   server. (Which native binary can download? Check LOLBAS/GTFOBins.)
2. [ ] Execute your payload through a trusted binary rather than running it directly.
3. [ ] Establish persistence using a native mechanism (scheduled task, registry, cron).
4. [ ] Switch hats: inspect the logs/telemetry and identify what *still* reveals your activity.

## Success criteria — you're done when
- [ ] You downloaded, executed, and persisted using only native binaries.
- [ ] You can name the LOLBins you used and what each normally does.
- [ ] You can point to the behavioural artifact that betrays the technique anyway.

## Deliverables
`lolbins.md`: the binaries used, the cradle → exec → persistence chain, and the telemetry that
detects it.

## AI acceleration
Have a model propose LOLBin techniques — then confirm each exists on your target and against
LOLBAS/GTFOBins before relying on it.

## Connects forward
This is the attacker side of Track 02 (detection engineering) and Track 07 (hardening /
allow-listing) — you're generating the exact behaviour they hunt.

## Marketable proof
> "I accomplish download/execute/persist using only native binaries (LOLBAS/GTFOBins) and can
> explain the behavioural detections that catch it."

## Automate & own it
**Required.** Script your LOLBin chain so it's reproducible, *and* note the matching detection
idea for each step (a mini attacker→defender map); AI drafts, you verify each binary; commit it.

## Stretch
- Take one technique and write the detection for it (a Sigma rule) — a direct preview of
  Track 02.
