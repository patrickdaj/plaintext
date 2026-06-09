# Lab 02 — Symmetric & AEAD

## Setup
This is a **reference lab** — it ships a one-command environment in the companion
[`plaintext-labs`](https://github.com/plaintext-security/plaintext-labs) repo:

```bash
git clone https://github.com/plaintext-security/plaintext-labs
cd plaintext-labs/cryptography/02-symmetric-aead
make up        # build the Python + OpenSSL container
make demo      # show CBC bit-flip, GCM authentication, and IV reuse attack
make shell     # drop into the container to work
make down      # stop when done
```

> Everything runs offline. No external dependencies.

## Scenario

Meridian's security audit team found a code path in the payroll API that reuses a hardcoded IV
for AES-GCM encryption. Before the developer team disputes the severity, your job is to
demonstrate concretely — in a controlled environment — what an attacker can do with two
ciphertexts encrypted under the same key and IV. Then implement the correct fix.

## Do

1. [ ] `make demo` — observe three demonstrations: (1) CBC bit-flip: an attacker modifies one
   block of CBC ciphertext and the next block decrypts to garbage — the confidentiality is
   corrupted but decryption succeeds. (2) GCM authentication: a tamper is detected. (3) GCM
   IV reuse: two ciphertexts with the same key/IV are XORed to reveal plaintext.

2. [ ] `make shell` and demonstrate the IV reuse attack manually:
   ```python
   python3 - <<'EOF'
   from cryptography.hazmat.primitives.ciphers.aead import AESGCM
   import os

   key = os.urandom(32)
   bad_iv = b'\x00' * 12   # hardcoded IV — the bug

   msg1 = b"Salary: $95,000 "
   msg2 = b"Budget: $200,000"

   ct1 = AESGCM(key).encrypt(bad_iv, msg1, None)
   ct2 = AESGCM(key).encrypt(bad_iv, msg2, None)

   # XOR the ciphertexts (excluding the 16-byte tag):
   xor_ct = bytes(a ^ b for a, b in zip(ct1[:16], ct2[:16]))
   print("XOR of ciphertexts:", xor_ct.hex())
   print("XOR of plaintexts: ", bytes(a ^ b for a, b in zip(msg1, msg2)).hex())
   print("Match:", xor_ct == bytes(a ^ b for a, b in zip(msg1, msg2)))
   EOF
   ```
   The XOR of the ciphertexts equals the XOR of the plaintexts. What does an attacker do with
   this? (Crib-dragging: if they know one message, they can recover the other.)

3. [ ] Implement the fix — correct IV generation:
   ```python
   python3 - <<'EOF'
   from cryptography.hazmat.primitives.ciphers.aead import AESGCM
   import os, json, base64

   key = os.urandom(32)
   msg = b"Salary: $95,000 for Q3 payroll"

   # Correct: random IV per encryption
   iv = os.urandom(12)
   ct = AESGCM(key).encrypt(iv, msg, None)

   # Serialise with IV prepended
   payload = json.dumps({
       "iv": base64.b64encode(iv).decode(),
       "ct": base64.b64encode(ct).decode()
   })
   print("Encrypted payload:", payload)
   EOF
   ```
   Note that the IV is random and transmitted with the ciphertext — it is not secret.

4. [ ] Add Associated Data (the AAD parameter) to the GCM call:
   ```python
   aad = b"recipient:payroll-service"   # authenticated, not encrypted
   ct = AESGCM(key).encrypt(iv, msg, aad)
   # Verify decryption fails if AAD is modified:
   try:
       AESGCM(key).decrypt(iv, ct, b"recipient:attacker")
   except Exception as e:
       print("AAD mismatch rejected:", e)
   ```
   What does AAD protect against? Write a one-paragraph explanation.

5. [ ] Repeat the nonce-reuse XOR demonstration with the fixed version (random IV). Confirm
   that two properly-encrypted messages cannot be XORed to reveal plaintexts.

## Success criteria — you're done when

- [ ] You demonstrated the IV reuse attack produces `xor_ct == xor_pt`.
- [ ] You implemented the correct random-IV pattern and confirmed it's unique per call.
- [ ] You added and tested AAD and can explain what it protects against.
- [ ] You understand why `ct1 XOR ct2 = pt1 XOR pt2` when the IV is reused.

## Deliverables

`aead-demo.py` — a script that demonstrates the IV reuse attack *and* the correct fix, with
comments explaining each step. Commit it.

## Automate & own it

**Required.** Write a Python script `check-iv-reuse.py` that takes a JSONL file of `{iv, ct}`
records and checks for duplicate IVs — flagging any reused IV as a critical finding. Have an
AI draft the duplicate-detection logic; you verify it handles the case of two identical IVs in
a large file correctly, and that it is case-insensitive to hex encoding.

## AI acceleration

Ask an AI: "Explain crib-dragging on XORed plaintexts — if I know that pt1 starts with
'Salary:', what can I recover about pt2?" Use the answer to extend the attack demo: add a
crib-drag step that recovers the salary amount from the XOR output. Verify the arithmetic
manually before committing.

## Connects forward

The IV uniqueness requirement and AAD concept you practiced here appear in TLS 1.3's record
layer (module 05) — TLS uses a sequence number as the nonce, ensuring uniqueness per session.
Module 10 (auditing crypto failures) returns to IV reuse as a real audit finding.

## Marketable proof

> "I demonstrated the GCM nonce-reuse attack — showing two same-IV ciphertexts XOR to reveal
> plaintext — and implemented the correct random-IV pattern with associated data authentication."

## Stretch

- Implement ChaCha20-Poly1305 encryption using the `cryptography` library and encrypt the same
  message. Compare the ciphertext size, the nonce size, and the API to AES-GCM. When would you
  choose ChaCha20-Poly1305 over AES-GCM?
- Research XSalsa20 and NaCl/libsodium's `secretbox`. How does libsodium's API prevent nonce
  reuse compared to a raw GCM API call? What is its nonce size and why?
