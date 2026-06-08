# Module 07 — Web Attacks: Authentication & Access Control

**Offensive Security** — *broken access control is OWASP's #1 risk for a reason.*

## Why this matters
Most web apps get the flashy bugs right and the boring ones wrong: weak authentication,
broken session handling, and — above all — broken access control, where you simply ask for
data that isn't yours and the server hands it over. It tops the OWASP Top 10 because it's
everywhere and trivially exploited. Finding it is mostly discipline, not cleverness.

## Objective
Identify and exploit authentication and access-control flaws — including IDOR and privilege
escalation — and explain the fix.

## Learn (~4 hrs)

**Hands-on labs**
- [PortSwigger — Authentication vulnerabilities](https://portswigger.net/web-security/authentication) — credential, session, and MFA flaws, with labs.
- [PortSwigger — Access control & IDOR](https://portswigger.net/web-security/access-control) — the highest-value, most common class.

**Reference**
- [OWASP Top 10 — A01: Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) — why it's ranked #1, with real examples.

## Key concepts
- Authentication vs authorization (the distinction that matters here)
- Insecure Direct Object References (IDOR)
- Vertical vs horizontal privilege escalation
- Session handling and token flaws
- The fix: enforce access control server-side, deny by default

## AI acceleration
A model helps you reason about which object IDs or roles to try — but access-control testing
is about methodically checking *every* action as *every* role, which a model won't do for
you. Use it to brainstorm; you do the disciplined enumeration.
