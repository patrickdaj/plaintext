# Lab 04 — Hashing, Encryption, and Certificates with openssl

## Setup
Docker-first:
```bash
docker run --rm -it alpine sh
apk add openssl
```

## Scenario
Exercise each primitive once so its guarantee becomes concrete rather than abstract.

## Do
1. [ ] Hash for integrity:
   ```bash
   echo "transfer 100 to alice" > msg.txt
   openssl dgst -sha256 msg.txt
   ```
2. [ ] Symmetric round-trip (AES):
   ```bash
   openssl enc -aes-256-cbc -pbkdf2 -in msg.txt -out msg.enc
   openssl enc -d -aes-256-cbc -pbkdf2 -in msg.enc
   ```
3. [ ] Asymmetric (RSA):
   ```bash
   openssl genrsa -out priv.pem 2048
   openssl rsa -in priv.pem -pubout -out pub.pem
   openssl pkeyutl -encrypt -pubin -inkey pub.pem -in msg.txt -out msg.rsa
   openssl pkeyutl -decrypt -inkey priv.pem -in msg.rsa
   ```
4. [ ] Inspect a real certificate (needs outbound network):
   ```bash
   echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
     | openssl x509 -noout -issuer -subject -dates
   ```
5. [ ] Flip one byte of `msg.enc` and try to decrypt it — observe.

## Success criteria — you're done when
- [ ] You produce a SHA-256 digest and can say why it proves integrity, not secrecy.
- [ ] You round-trip a message through both AES and RSA.
- [ ] You can read a certificate's issuer, subject, and validity, and name who vouches for it.

## Deliverables
`crypto-notes.md`: one line per primitive — what it guaranteed — plus what happened when
you flipped a byte of the AES ciphertext.

## AI acceleration
Ask a model why CBC without authentication is unsafe and what AES-GCM fixes — then confirm
against the OpenSSL Cookbook, noting anywhere it gets the flags wrong.

## Connects forward
This underpins Track 05 (TLS and secrets in the cloud), Track 08 (PKI and secrets in
depth), and any HTTPS you inspect in Track 01.

## Marketable proof
> "I can exercise and audit the core crypto primitives with openssl — hashing, AES, RSA,
> and a live certificate chain — and explain what each does and doesn't guarantee."

## Stretch
- Redo the symmetric step with `-aes-256-gcm` (AEAD) and explain what the authentication
  tag changes.
