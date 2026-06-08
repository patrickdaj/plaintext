# Module 08 — Web Attacks: SSRF, XXE & Deserialization

**Offensive Security** — *the server-side classes that turn one web bug into cloud compromise.*

## Why this matters
Beyond the client-facing bugs lie the server-side ones — Server-Side Request Forgery, XML
External Entity injection, and insecure deserialization — that let an attacker make the
server itself act on their behalf. SSRF against a cloud metadata endpoint is exactly how the
2019 Capital One breach exposed 100M+ records, which is why these classes matter far more than
their frequency suggests.

## Objective
Identify and exploit SSRF, XXE, and insecure deserialization against deliberately vulnerable
apps, and explain each root cause and fix.

## Learn (~4 hrs)

**Hands-on labs**
- [PortSwigger — Server-Side Request Forgery (SSRF)](https://portswigger.net/web-security/ssrf) — including the cloud-metadata pattern behind Capital One.
- [PortSwigger — XXE injection](https://portswigger.net/web-security/xxe) — abusing XML parsers.
- [PortSwigger — Insecure deserialization](https://portswigger.net/web-security/deserialization) — turning serialized objects into code execution.

## Key concepts
- SSRF and the cloud metadata endpoint (`169.254.169.254`)
- XXE: external entities, file read, and SSRF via XML
- Insecure deserialization → remote code execution
- Why these pivot from "web bug" to "infrastructure compromise"
- The fixes: allow-lists, disabling external entities, avoiding/signing deserialization

## AI acceleration
A model explains these abstract classes and drafts payloads well — but exploiting them
reliably needs you to understand the target's parser, network position, and trust
relationships, which the model can't see. Use it to learn the class; verify the exploit
against the actual app.
