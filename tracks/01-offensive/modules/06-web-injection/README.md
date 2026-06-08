# Module 06 — Web Attacks: Injection

**Offensive Security** — *the injection class that still pops databases decades later.*

## Why this matters
Injection — SQL and OS command — happens whenever untrusted input is treated as code. It's
behind some of the largest breaches in history and remains everywhere because it's a design
mistake, not a single bug. Learning to find and exploit it (and later to fix it) is core
web-security literacy.

## Objective
Find and exploit SQL injection and command injection against a deliberately vulnerable app,
and explain the root cause and the fix.

## Learn (~4 hrs)

**Hands-on labs**
- [PortSwigger Web Security Academy — SQL injection](https://portswigger.net/web-security/sql-injection) — the best free, hands-on labs anywhere; do the apprentice-level set.
- [PortSwigger — OS command injection](https://portswigger.net/web-security/os-command-injection) — the sibling class.

**Reference**
- [OWASP — SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) — the canonical explanation and defenses.

## Key concepts
- Injection root cause: data treated as code
- UNION-based, error-based, and blind SQLi
- OS command injection
- Automating with `sqlmap` (and why you must understand it first)
- The fix: parameterised queries / safe APIs

## AI acceleration
A model writes injection payloads and explains an error message fast — useful when you're
stuck. But it also produces payloads that don't fit the context or that you can't explain; in
an engagement, a finding you can't reproduce and explain is worthless. Understand every
payload you fire.
