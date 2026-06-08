# Lab 15 — Walk a Real Cloud Pentest

## Setup
A browser for [flaws.cloud](http://flaws.cloud/) (no account needed), and/or your own AWS
free-tier account with [CloudGoat](https://github.com/RhinoSecurityLabs/cloudgoat) +
[Pacu](https://github.com/RhinoSecurityLabs/pacu) for a deployable scenario.

## Scenario
Work a real, intentionally vulnerable cloud target from initial misconfiguration to
credential/data access.

> Use flaws.cloud (built for this) or your own account/CloudGoat. Never test accounts or
> tenants you don't own, and tear down billable resources when done.

## Do
1. [ ] Start flaws.cloud and find the first misconfiguration (an open S3 bucket). What did
   public access leak?
2. [ ] Follow the chain: use what you find (keys, bucket contents) to reach the next level.
3. [ ] Identify at least one IAM/privilege issue and explain how it escalates access.
4. [ ] Tie it back: explain how a web SSRF (module 08) reaching the metadata endpoint would
   yield the same credentials.

## Success criteria — you're done when
- [ ] You progressed through multiple flaws.cloud levels (or a CloudGoat scenario).
- [ ] You can explain the misconfiguration at each step and its fix.
- [ ] You can connect SSRF → metadata → credentials in your own words.

## Deliverables
`cloud-primer.md`: the chain you walked, the misconfig + fix at each step, and the
SSRF-to-metadata link.

## AI acceleration
Use a model to decode IAM policies and AWS errors — then verify against AWS docs. Cloud is
where a confident-wrong answer can touch a billable, real account.

## Connects forward
This is the on-ramp to Track 05 (Cloud & Container Security), which does posture, IaC, and
Kubernetes in depth.

## Marketable proof
> "I walk a real cloud attack chain — open storage, leaked keys, IAM escalation,
> SSRF-to-metadata — and explain the fix at each step."

## Automate & own it
**Required.** Script one step (e.g. enumerate the open bucket, or pull and parse the instance
metadata) in Python/CLI; AI drafts, you verify against the docs; commit it.

## Stretch
- Deploy a CloudGoat scenario and exploit it with Pacu end to end, then destroy it.
