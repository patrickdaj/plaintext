# Lab 09 — Crack Real Password Hashes

## Setup

```bash
git clone https://github.com/plaintext-security/plaintext-labs.git
cd plaintext-labs/offensive/09-password-attacks
make up
```

The lab container has Python + passlib + bcrypt; no GPU required. The bundled
`data/hashes.txt` contains 11 hashes from a simulated Meridian Financial dump
(MD5, NTLM, bcrypt, SHA-256, SHA-1) — passwords drawn from rockyou.txt.

## Scenario

You've exfiltrated a credential dump from Meridian Financial's internal
identity store. Crack it the way an attacker would: identify hash types,
run a dictionary attack, apply rules-based mutations, then assess what
defenses would have stopped you.

> **Authorization note:** Only crack hashes you generated or are authorised to
> test. Never attack credentials you don't own.

## Do

1. [ ] Run the demo to see the full cracking pipeline:
   ```bash
   make demo
   ```
   Review: which hashes fell to the dictionary, which to rules, which stood.

2. [ ] Identify each hash type before cracking. Open `data/hashes.txt` and note:
   - How do you tell NTLM from MD5 by inspection alone?
   - Why does bcrypt start with `$2b$12$…`?
   - What does the `aad3b435…` NTLM hash tell you without cracking it?

3. [ ] Trace the dictionary attack in `crack.py`. Understand the flow:
   `load_hashes()` → `crack_hash()` → `ntlm()`/`md5()` → compare.

4. [ ] Explain why 8/11 hashes cracked in milliseconds but bcrypt did not.
   Review the KDF comparison output (Step 4) — what is the cost factor doing?

5. [ ] Run with rules enabled and observe which additional hashes (if any) fall.
   What mutations does `apply_rules()` try, and why are they realistic?

6. [ ] Write the three defenses you'd recommend Meridian adopt, ranked by impact.

## Success criteria — you're done when

- [ ] You can identify hash types from format alone (bcrypt vs NTLM vs SHA-256).
- [ ] You understand *why* MD5/SHA-1 are broken for passwords (speed, not just length).
- [ ] You cracked ≥8/11 hashes and can explain the ones that resisted.
- [ ] You can state the defenses (slow KDF ≥ cost 12, salt, length ≥ 15, MFA) that defeat offline cracking.

## Deliverables

`cracking.md`: hash types identified, which cracked (mode + time), and the three
defenses you'd prioritise for Meridian. (Don't commit real wordlists or raw dumps.)

## Automate & own it

**Required.** Extend `crack.py` or write a new `auto_crack.py` that:
- Reads a hash file
- Auto-identifies hash types
- Selects the right algorithm
- Outputs a Markdown report with crack results + recommended mitigations

AI drafts the script; you review every function before committing. Commit
`auto_crack.py` and your `cracking.md` alongside it.

## AI acceleration

Ask a model to identify a hash from its format and suggest the hashcat mode —
then verify before you spend GPU time. A wrong mode is hours wasted.
Also: prompt a model to generate a contextual wordlist for "Meridian Financial"
(company names, financial jargon) and check what it adds to the hit rate.

## Connects forward

Cracked credentials feed lateral movement (module 12). In the Active Directory
track, Kerberoasting hands you crackable service-ticket hashes the same way —
same cracking pipeline, same KDF weakness, just a different dump vector.

## Marketable proof

> "I crack real password hashes — identifying types, choosing attack modes, applying
> rules-based mutations — and can argue the hashing and MFA defenses that defeat it."

## Stretch

- Crack a captured NTLMv2 hash (Responder output) — note how `Net-NTLMv2`
  differs from an NTLM database dump.
- Benchmark the full rockyou.txt against MD5 (extrapolate from the KDF comparison)
  and argue when a GPU cluster changes the calculus.
