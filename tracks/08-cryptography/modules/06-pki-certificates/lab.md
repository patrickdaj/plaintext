# Lab 06 — PKI & Certificate Management

## Setup
This is a **reference lab** — it ships a one-command environment in the companion
[`plaintext-labs`](https://github.com/plaintext-security/plaintext-labs) repo:

```bash
git clone https://github.com/plaintext-security/plaintext-labs
cd plaintext-labs/cryptography/06-pki-certificates
make up        # start step-ca container
make demo      # init CA, issue leaf cert, verify chain, show OCSP revocation
make shell     # drop into the container to work
make down      # stop when done
```

> Everything runs locally. No internet connection required.

## Scenario

Meridian Financial is deploying mutual TLS (mTLS) between its internal microservices. Your
job: stand up a private CA with `step-ca`, issue service certificates, verify the chain, and
demonstrate certificate revocation — the complete PKI lifecycle for an mTLS programme.

## Do

1. [ ] `make demo` — watch the full sequence: CA initialisation, leaf certificate issuance,
   chain verification, OCSP query, and revocation. Note the certificate fields printed at
   each step.

2. [ ] `make shell` and initialise a fresh CA (the demo has already done this — re-examine it):
   ```bash
   step ca certificate meridian.internal /tmp/leaf.crt /tmp/leaf.key \
     --ca-url https://localhost:8443 \
     --root /home/step/.step/certs/root_ca.crt \
     --provisioner admin@meridian.internal
   ```
   Inspect the issued certificate:
   ```bash
   step certificate inspect /tmp/leaf.crt
   openssl x509 -in /tmp/leaf.crt -text -noout | grep -A5 "Subject Alternative"
   openssl x509 -in /tmp/leaf.crt -text -noout | grep -A2 "Validity"
   ```
   What is the default validity period? What SAN is included?

3. [ ] Verify the certificate chain:
   ```bash
   step certificate verify /tmp/leaf.crt \
     --roots /home/step/.step/certs/root_ca.crt
   echo "Chain verification: $?"
   ```
   Now corrupt the certificate slightly and try again:
   ```bash
   python3 -c "
   data = open('/tmp/leaf.crt').read()
   data = data.replace('CERTIFICATE', 'CERT1F1CATE')
   open('/tmp/corrupt.crt','w').write(data)
   "
   step certificate verify /tmp/corrupt.crt \
     --roots /home/step/.step/certs/root_ca.crt 2>&1
   ```
   What error does the chain verification produce?

4. [ ] Revoke the leaf certificate:
   ```bash
   step ca revoke $(step certificate fingerprint /tmp/leaf.crt) \
     --ca-url https://localhost:8443 \
     --root /home/step/.step/certs/root_ca.crt
   ```
   Then query OCSP to confirm the revocation status:
   ```bash
   step ca certificate-status /tmp/leaf.crt \
     --ca-url https://localhost:8443 \
     --root /home/step/.step/certs/root_ca.crt
   ```
   What status is returned? What serial number does the revoked certificate have?

5. [ ] Issue a second certificate with a short validity period (5 minutes):
   ```bash
   step ca certificate payroll.internal /tmp/short.crt /tmp/short.key \
     --ca-url https://localhost:8443 \
     --root /home/step/.step/certs/root_ca.crt \
     --provisioner admin@meridian.internal \
     --not-after 5m
   openssl x509 -in /tmp/short.crt -noout -dates
   ```
   What is the `notAfter` timestamp? Why do short-lived certificates reduce reliance on
   revocation?

6. [ ] Inspect the root CA certificate and identify: the `basicConstraints` extension (CA:TRUE),
   the `keyUsage` extension (keyCertSign, cRLSign), and the self-signed signature. Write a
   one-paragraph explanation of why these extensions distinguish a CA certificate from a leaf.

## Success criteria — you're done when

- [ ] You issued a leaf certificate and verified the chain against the root CA.
- [ ] You confirmed that a corrupted certificate fails chain verification.
- [ ] You revoked a certificate and confirmed the OCSP response shows "revoked".
- [ ] You issued a short-lived (5-minute) certificate and can explain why it reduces revocation dependence.

## Deliverables

`pki-analysis.md` — the certificate fields (SAN, validity, basicConstraints) from your leaf
cert, the revocation evidence (serial number + OCSP response), and the short-lived certificate
argument. Commit it.

## Automate & own it

**Required.** Write a shell script `cert-expiry-check.sh` that: takes a certificate file as
argument, reads the `notAfter` date with `openssl x509 -noout -enddate`, and exits non-zero
if the certificate expires within 30 days. Have an AI draft the date arithmetic in bash or
Python; you verify the exit code is correct for both "expiring soon" and "valid for 6 months"
cases.

## AI acceleration

Ask an AI: "What does the X.509 basicConstraints extension do, and why is `CA:FALSE` on a
leaf certificate important for preventing mis-issuance?" Verify the answer against RFC 5280
Section 4.2.1.9. Then check your issued leaf certificate to confirm `CA:FALSE` is set
(`openssl x509 -text -in /tmp/leaf.crt -noout | grep "CA:"`).

## Connects forward

The private CA you stood up here is the trust anchor for the mTLS configuration that the
track capstone deploys. Module 10 (Auditing Applied-Crypto Failures) includes certificate
audit checks — expired certificates, weak signature algorithms, missing OCSP stapling — as a
structured finding category.

## Marketable proof

> "I stood up a step-ca private CA, issued and revoked certificates, verified the chain, and
> demonstrated OCSP-based revocation — the PKI lifecycle for an internal mTLS programme."

## Stretch

- Configure an ACME provisioner in step-ca and use `certbot` (or `step` in ACME mode) to
  automatically issue and renew a certificate. This is the automation pattern that eliminates
  manual certificate management.
- Research Certificate Transparency (CT): what is a CT log, why does Chrome require certificates
  to be CT-logged, and what is the security benefit? Look up `step-ca`'s CT integration.
