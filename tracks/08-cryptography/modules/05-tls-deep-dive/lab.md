# Lab 05 — TLS Deep Dive

## Setup
This is a **reference lab** — it ships a one-command environment in the companion
[`plaintext-labs`](https://github.com/plaintext-security/plaintext-labs) repo:

```bash
git clone https://github.com/plaintext-security/plaintext-labs
cd plaintext-labs/cryptography/05-tls-deep-dive
make up        # build nginx with weak config + testssl.sh container
make demo      # scan the weak config, show findings, switch to strong config, rescan
make shell     # drop into the testssl container
make down      # stop when done
```

> Everything runs locally. The nginx server is on the Docker bridge network — no external
> connections needed.

## Scenario

Meridian Financial's external security assessment found their internal API gateway is running
nginx with TLS 1.0 enabled and several weak cipher suites. You have been asked to: reproduce
the assessment findings, understand each one, apply the Mozilla "modern" TLS profile, and
rescan to confirm the findings are resolved.

## Do

1. [ ] `make demo` — watch testssl.sh scan the weak nginx configuration. Record: which TLS
   versions are supported, which cipher suites are flagged, and any certificate findings.

2. [ ] `make shell` and scan the weak nginx manually:
   ```bash
   testssl.sh --severity HIGH nginx:443 2>/dev/null | tee /tmp/weak-results.txt
   grep -E "(HIGH|CRITICAL|MEDIUM)" /tmp/weak-results.txt
   ```
   For each HIGH or CRITICAL finding: which cipher suite or setting causes it, and what
   property does it undermine (forward secrecy, authentication, confidentiality)?

3. [ ] Inspect the weak nginx TLS configuration (`data/nginx-weak.conf`) and identify the
   specific directives that produce each finding. Common culprits:
   - `ssl_protocols TLSv1 TLSv1.1 TLSv1.2;` — TLS 1.0/1.1 enabled.
   - `ssl_ciphers RC4:...` or `ssl_ciphers HIGH:!aNULL` — includes weak ciphers.

4. [ ] Apply the Mozilla modern profile. Edit `data/nginx-strong.conf` to use:
   ```nginx
   ssl_protocols TLSv1.3;
   ssl_ciphers TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256;
   ssl_prefer_server_ciphers off;
   add_header Strict-Transport-Security "max-age=63072000" always;
   ```
   Reload nginx with the strong config (the Makefile has a `reload-strong` target) and rescan:
   ```bash
   testssl.sh --severity HIGH nginx:443 2>/dev/null | tee /tmp/strong-results.txt
   grep -E "(HIGH|CRITICAL|MEDIUM)" /tmp/strong-results.txt
   ```
   How many findings remain?

5. [ ] Inspect the TLS handshake manually with OpenSSL:
   ```bash
   # Connect and show negotiated cipher and protocol:
   openssl s_client -connect nginx:443 -tls1_3 < /dev/null 2>&1 \
     | grep -E "(Protocol|Cipher|Certificate chain)"
   ```
   What cipher suite was negotiated? Which key exchange algorithm? Is it ECDHE (forward secret)?

6. [ ] Write `tls-audit-report.md`: a table with finding name, severity, affected property,
   weak config directive, and strong config fix for the top five findings.

## Success criteria — you're done when

- [ ] You identified the weak config's HIGH/CRITICAL findings and their root causes.
- [ ] You applied the Mozilla modern profile and confirmed the findings are resolved.
- [ ] You used `openssl s_client` to inspect the negotiated cipher and protocol.
- [ ] You produced a `tls-audit-report.md` with finding → root cause → fix.

## Deliverables

`tls-audit-report.md` — your five-finding table. Commit it.

## Automate & own it

**Required.** Write a shell script `tls-check.sh` that runs `testssl.sh` against a host:port,
parses the output for HIGH and CRITICAL severity findings, and exits non-zero if any are
found. Wire it into a GitHub Actions workflow that runs the check against a test endpoint on
every PR. Have an AI draft the grep/awk parsing; you verify the exit code is non-zero when
HIGH findings are present.

## AI acceleration

Paste the testssl.sh output line for a specific HIGH finding into an AI and ask: "What is
this TLS finding, what can an attacker do if this is present, and what is the nginx
configuration change that fixes it?" Verify the nginx fix against the Mozilla SSL
Configuration Generator output for the "modern" profile.

## Connects forward

The cipher suite knowledge from this module is the foundation for module 06 (PKI & Certificate
Management) — a properly configured CA needs to issue certificates with strong signature
algorithms — and module 10 (Auditing Applied-Crypto Failures), where you audit a matrix of
TLS configurations and score the delta.

## Marketable proof

> "I ran testssl.sh against a weak TLS configuration, identified HIGH/CRITICAL findings,
> applied the Mozilla modern TLS profile, and confirmed all findings were resolved — producing
> an audit evidence report."

## Stretch

- Use Wireshark (or `tcpdump + tshark`) to capture the TLS 1.3 handshake and decode the
  ClientHello. Identify: supported groups, signature algorithms, and ALPN extensions. What
  does the ServerHello contain?
- Research HSTS preloading: what is `includeSubDomains` and `preload` in the
  `Strict-Transport-Security` header, what is the preload list, and what is the risk of
  submitting a domain before you're ready?
