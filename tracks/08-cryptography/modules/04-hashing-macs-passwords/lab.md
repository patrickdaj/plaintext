# Lab 04 — Hashing, MACs & Passwords

*Hands-on lab · [← Back to the module concept](README.md)*


## Setup
This is a **reference lab** — it ships a one-command environment in the companion
[`plaintext-labs`](https://github.com/plaintext-security/plaintext-labs) repo:

```bash
git clone https://github.com/plaintext-security/plaintext-labs
cd plaintext-labs/cryptography/04-hashing-macs-passwords
make up        # build the Python + OpenSSL + argon2 container
make demo      # show SHA-256 hash, HMAC-SHA256, Argon2id hash, and cracking exercise
make shell     # drop into the container to work
make down      # stop when done
```

> Everything runs offline. No external dependencies.

## Scenario

Meridian Financial's legacy payroll application stores employee passwords as unsalted SHA-256
hashes. A penetration test extracted the hash database. Your job: demonstrate how quickly an
unsalted SHA-256 database can be cracked, then implement Argon2id storage, and show the
cracking cost difference.

## Do

1. [ ] `make demo` — observe: SHA-256 hashes computed for the sample passwords, HMAC-SHA256
   with a key, Argon2id hashes with tuned parameters, and a simulated crack attempt against
   the SHA-256 hashes.

2. [ ] `make shell` and crack the unsalted SHA-256 hashes using the wordlist:
   ```bash
   python3 - <<'EOF'
   import hashlib

   # Simulate the leaked database (unsalted SHA-256):
   db = {}
   with open('/lab/data/passwords.txt') as f:
       for line in f:
           pwd = line.strip()
           db[hashlib.sha256(pwd.encode()).hexdigest()] = pwd

   # Simulate hashes extracted from the application:
   targets = [
       hashlib.sha256(b"password123").hexdigest(),
       hashlib.sha256(b"meridian2024").hexdigest(),
       hashlib.sha256(b"Tr0ub4dor&3").hexdigest(),   # from the wordlist
   ]

   print("Cracking results:")
   for h in targets:
       result = db.get(h, "NOT FOUND")
       print(f"  {h[:16]}... => {result}")
   EOF
   ```
   How many of the three target hashes were cracked? What would a GPU-backed crack do with the
   full wordlist?

3. [ ] Hash the same passwords with Argon2id and observe the cost:
   ```python
   python3 - <<'EOF'
   import time
   from argon2 import PasswordHasher

   ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2)

   passwords = ["password123", "meridian2024", "Tr0ub4dor&3"]
   for pwd in passwords:
       start = time.perf_counter()
       h = ph.hash(pwd)
       elapsed = time.perf_counter() - start
       print(f"Hashed '{pwd}' in {elapsed:.3f}s: {h[:40]}...")
   EOF
   ```
   What is the per-hash cost? How many Argon2id hashes per second can this container compute?
   Compare that to the SHA-256 cracking rate.

4. [ ] Verify an Argon2id hash:
   ```python
   python3 - <<'EOF'
   from argon2 import PasswordHasher
   from argon2.exceptions import VerifyMismatchError

   ph = PasswordHasher()
   h = ph.hash("correct-password")
   print("Hash:", h[:50], "...")

   # Correct password:
   try:
       ph.verify(h, "correct-password")
       print("Verification: SUCCESS")
   except VerifyMismatchError:
       print("Verification: FAILED")

   # Wrong password:
   try:
       ph.verify(h, "wrong-password")
   except VerifyMismatchError:
       print("Wrong password: rejected")
   EOF
   ```

5. [ ] Compute an HMAC-SHA256 for message integrity (not password storage):
   ```bash
   echo -n "Payroll batch 2026-06-01: total=$1234567.89" \
     | openssl mac -digest SHA256 -macopt key:supersecrethmackey HMAC
   ```
   Modify one character of the message and recompute. Do the HMACs match? Why is HMAC
   appropriate here but not for password storage?

## Success criteria — you're done when

- [ ] You cracked at least two of the three unsalted SHA-256 hashes using the wordlist.
- [ ] You measured the Argon2id hashing rate and can state the orders-of-magnitude difference.
- [ ] You verified Argon2id accepts the correct password and rejects the wrong one.
- [ ] You can explain in one paragraph why HMAC is the right tool for message integrity but not password storage.

## Deliverables

`password-analysis.md` — your cracking results (how many cracked, how fast), the Argon2id
timing (hashes per second), and a one-page argument for migrating Meridian's password storage
from SHA-256 to Argon2id including work factor recommendation. Commit it.

## Automate & own it

**Required.** Write a Python script `check-password-hash.py` that reads a file of stored hashes
and flags any that are identifiable as MD5, SHA-1, or SHA-256 by their length and format (no
salt, no algorithm identifier prefix). Output: "VULNERABLE: N passwords stored as <algorithm>".
Have an AI draft the pattern-matching logic; you verify it correctly identifies `$argon2id$`
prefixed hashes as "OK" and bare hex strings as vulnerable.

## AI acceleration

Ask an AI: "What Argon2id time_cost, memory_cost, and parallelism settings are appropriate for
a login endpoint that should take ~200ms per hash on 2 CPU cores with 512MB available?" Use the
OWASP Password Storage Cheat Sheet to validate the recommendation. Then test it in the container
and measure the actual elapsed time.

## Connects forward

The password hash principles here are directly applied in module 07 (Secrets Management) —
Vault's internal authentication uses bcrypt, and knowing why matters. Module 10 (Auditing
Applied-Crypto Failures) includes finding unsalted or weak password hashes as an audit check.

## Marketable proof

> "I demonstrated the difference between unsalted SHA-256 (cracked in milliseconds) and Argon2id
> (computation-bounded by design), and wrote a migration recommendation for Meridian's password
> storage with tuned work factor parameters."

## Stretch

- Implement the [Have I Been Pwned k-anonymity API](https://haveibeenpwned.com/API/v3#SearchingPwnedPasswordsByRange):
  hash a password with SHA-1, send the first 5 hex characters to the API, check if your hash
  appears in the response. This is the production pattern for checking passwords without
  revealing them to the service.
- Research rainbow tables: how does a salt specifically defeat them? Write a one-paragraph
  explanation, then verify your understanding by showing that two Argon2id hashes of the same
  password produce different outputs (different salts).
