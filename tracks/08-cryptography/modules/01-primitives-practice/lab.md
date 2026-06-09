# Lab 01 — Primitives in Practice

## Setup
This is a **reference lab** — it ships a one-command environment in the companion
[`plaintext-labs`](https://github.com/plaintext-security/plaintext-labs) repo:

```bash
git clone https://github.com/plaintext-security/plaintext-labs
cd plaintext-labs/cryptography/01-primitives-practice
make up        # build the OpenSSL container
make demo      # encrypt with AES-CBC, then AES-GCM; show tamper detection
make shell     # drop into the container to work
make down      # stop when done
```

> Everything runs offline in a container you own. No external dependencies.

## Scenario

Meridian Financial's development team is debating whether to use AES-CBC or AES-GCM for
encrypting customer data at rest. Before the architecture review, your job is to demonstrate
concretely what guarantee each mode provides — including what an attacker can do to CBC that
they cannot do to GCM — so the team makes an informed choice.

## Do

1. [ ] `make demo` — watch the demo encrypt a file with AES-256-CBC and AES-256-GCM, then
   tamper with the ciphertext, then attempt decryption. Note: which mode detects the tampering,
   which silently decrypts corrupted data.

2. [ ] `make shell` and encrypt a plaintext file with AES-256-CBC manually:
   ```bash
   openssl enc -aes-256-cbc -in /lab/data/plaintext.txt -out /tmp/cipher-cbc.bin \
     -K 0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20 \
     -iv 0102030405060708090a0b0c0d0e0f10
   ```
   Now tamper with one byte of the ciphertext:
   ```bash
   python3 -c "
   data = bytearray(open('/tmp/cipher-cbc.bin','rb').read())
   data[32] ^= 0xFF  # flip bits in the second block
   open('/tmp/cipher-cbc-tampered.bin','wb').write(data)
   "
   # Decrypt the tampered ciphertext:
   openssl enc -d -aes-256-cbc -in /tmp/cipher-cbc-tampered.bin \
     -K 0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20 \
     -iv 0102030405060708090a0b0c0d0e0f10 2>/dev/null | xxd | head
   ```
   Did decryption succeed? What did the output look like? This is the "silent corruption" problem.

3. [ ] Now encrypt with AES-256-GCM:
   ```bash
   openssl enc -aes-256-gcm -in /lab/data/plaintext.txt -out /tmp/cipher-gcm.bin \
     -K 0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20 \
     -iv 010203040506070809000000
   ```
   Tamper with the ciphertext in the same way and attempt decryption:
   ```bash
   python3 -c "
   data = bytearray(open('/tmp/cipher-gcm.bin','rb').read())
   data[10] ^= 0xFF
   open('/tmp/cipher-gcm-tampered.bin','wb').write(data)
   "
   openssl enc -d -aes-256-gcm -in /tmp/cipher-gcm-tampered.bin \
     -K 0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20 \
     -iv 010203040506070809000000
   ```
   What error does OpenSSL return? This is authentication failure — the guarantee GCM provides.

4. [ ] Document the difference: write two paragraphs in `primitives-analysis.md`:
   - What happened when you tampered with the CBC ciphertext, and what this means for Meridian's data-at-rest design.
   - What happened when you tampered with the GCM ciphertext, and why this is the correct guarantee.

5. [ ] Use OpenSSL to compute an HMAC of the plaintext (MAC-then-encrypt pattern for reference):
   ```bash
   openssl mac -digest SHA256 -macopt key:supersecretkey HMAC < /lab/data/plaintext.txt
   ```
   Explain: why is HMAC-then-encrypt different from AES-GCM? Which provides a stronger
   guarantee and why? (Hint: read about Encrypt-then-MAC vs MAC-then-Encrypt.)

## Success criteria — you're done when

- [ ] You observed CBC silently decrypting tampered ciphertext.
- [ ] You observed GCM returning an authentication error on tampered ciphertext.
- [ ] You documented the difference in `primitives-analysis.md` with a recommendation.
- [ ] You computed an HMAC and can explain the MAC-then-encrypt vs AEAD distinction.

## Deliverables

`primitives-analysis.md` — your two-paragraph CBC vs GCM analysis plus the HMAC comparison.
Commit it.

## Automate & own it

**Required.** Write a Python script `encrypt-aead.py` that: takes a plaintext file and a key,
encrypts with AES-256-GCM using the `cryptography` library (not OpenSSL subprocess), and
outputs the IV, tag, and ciphertext as a JSON object. Have an AI draft the script using
`cryptography.hazmat.primitives`; you verify the IV is randomly generated (not hardcoded) and
the tag is included in the output before committing.

## AI acceleration

Ask an AI: "What is the difference between AES-CBC and AES-GCM from an attacker's perspective?"
Use the answer to check your own CBC tamper experiment against the explanation. Then ask a
follow-up: "What is the Padding Oracle attack on CBC?" — and verify the explanation against the
OWASP Padding Oracle page before including any claims in your deliverable.

## Connects forward

The AEAD guarantee you observed here is the foundation for module 02 (Symmetric & AEAD) which
explores IV reuse attacks, and module 05 (TLS Deep Dive) where GCM is the dominant cipher suite
in TLS 1.3. Module 10 (Auditing Applied-Crypto Failures) returns to these failure modes in the
context of real-world findings.

## Marketable proof

> "I demonstrated the concrete security difference between AES-CBC and AES-GCM by tampering
> with ciphertexts — showing CBC's silent corruption failure and GCM's authentication check —
> and wrote an architecture recommendation for Meridian's data-at-rest design."

## Stretch

- Encrypt the same plaintext with AES-128-ECB and look at the output for a structured input
  (e.g. a file with repeated 16-byte blocks). Observe the identical ciphertext blocks. This is
  the visual proof that ECB mode is broken.
- Research the difference between GCM authentication tag sizes (96-bit vs 128-bit) and when
  a truncated tag is acceptable. Write one paragraph on the trade-off.
