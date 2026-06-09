# Lab 08 — Exploit SSRF and XXE

*Hands-on lab · [← Back to the module concept](README.md)*


## Setup

```bash
git clone https://github.com/plaintext-security/plaintext-labs.git
cd plaintext-labs/offensive/08-web-ssrf-xxe
make up
```

The container runs a minimal Flask app (`app/app.py`) — Meridian Financial's
document portal — with two deliberate server-side bugs. A mock cloud metadata
server runs on `127.0.0.1:5001` inside the container, simulating what the
AWS Instance Metadata Service (169.254.169.254) looks like from an EC2 host.

## Scenario

Meridian's document portal has two features: a URL fetcher (for link previews)
and an XML invoice importer. Both features process server-supplied data without
validating the input source. Neither can be exploited from the UI — but the API
endpoints have no server-side trust boundary.

> **Authorization note:** Only exploit PortSwigger labs, deliberately vulnerable
> apps, or systems you own or have explicit written authorisation to test.

## Do

1. [ ] Run the demo to see both exploits:
   ```bash
   make demo
   ```
   Note what data each exploit extracts and what the fix would be.

2. [ ] Read `app/app.py`. Find the two vulnerable functions. For each:
   - What input does the server act on without validation?
   - What does "confused deputy" mean in context?
   - Which `urllib` / `lxml` arguments make it vulnerable?

3. [ ] Trace the SSRF (Bug 1) manually:
   - The server fetches `url=http://127.0.0.1:5001/...` on the attacker's behalf.
   - Why can't the attacker reach `127.0.0.1:5001` directly?
   - In AWS, this address would be `169.254.169.254`. What did Capital One's attacker
     do once they had the IAM credentials?

4. [ ] Trace the XXE (Bug 2) manually:
   - Paste the XXE payload into a file and run:
     ```bash
     make shell
     python3 -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/health').read())"
     ```
     Then craft a `curl` request with the XXE body.
   - Change `file:///etc/hostname` to `file:///etc/passwd`. What comes back?
   - How would you chain XXE to SSRF (use an `http://` entity instead of `file://`)?

5. [ ] Apply Bug 1's fix: edit `app/app.py` and add the URL allow-list. Re-run
   `make demo` and confirm the SSRF returns HTTP 403.

6. [ ] Apply Bug 2's fix: switch to `lxml.etree.XMLParser(resolve_entities=False,
   load_dtd=False)`. Re-run and confirm the XXE returns a parse error (no file read).

## Success criteria — you're done when

- [ ] You made the server fetch internal credentials via SSRF (simulated IMDSv1).
- [ ] You injected an XXE entity to read a local file from the server's filesystem.
- [ ] You applied both fixes and confirmed each returns the right error.
- [ ] You can explain the "confused deputy" model and how SSRF + XXE share the same root cause.
- [ ] You can describe the IMDSv2 change that mitigates the Capital One-style SSRF.

## Deliverables

`ssrf-xxe.md`: for each bug — the vulnerable code snippet, the exploit payload,
the response that proved it, and the fixed code. One sentence linking SSRF to
the Capital One breach and explaining why IMDSv2's PUT-first flow helps.

## Automate & own it

**Required.** Write `probe.py` that:
- Takes a target URL as an argument
- Probes a list of internal addresses (127.0.0.1, common RFC 1918 ranges, 169.254.x.x)
  via the `/api/fetch?url=` parameter
- Reports which internal addresses responded

AI drafts the probe list and loop; you reason about what the server's network
can actually reach and annotate each result. Commit `probe.py` and `ssrf-xxe.md`.

## AI acceleration

Ask a model to explain why IMDSv2 (PUT request to get a session token first)
makes the Capital One SSRF harder — and then verify by reading the AWS docs.
The model explains the control; you verify the mechanism against the spec.

## Connects forward

SSRF to the metadata service is the bridge from "web pentesting" to cloud
compromise. Track 05 (cloud) picks up from here — IAM privilege escalation,
S3 misconfiguration, and cloud-specific attack paths all start from leaked
credentials or reachable metadata services.

## Marketable proof

> "I exploit SSRF and XXE — the server-side classes behind the Capital One
> breach — and can explain the allow-list and parser-hardening fixes, plus why
> IMDSv2 raises the bar for cloud SSRF."

## Stretch

- Research what the Capital One attacker did after obtaining IAM credentials
  (CVE-2019-5736 is unrelated; look at the 2019 Capital One breach report).
  What S3 permissions did the EC2 role have?
- Chain XXE to SSRF: replace `file:///etc/hostname` with
  `http://127.0.0.1:5001/latest/meta-data/iam/security-credentials/`
  in the entity declaration. Does the XML parser fetch it?
