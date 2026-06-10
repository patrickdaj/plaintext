# Verify a Plaintext Certificate

Paste a learner's `certificate.json` (or a single lab `receipt.json`) below to check that it is
**internally consistent and unedited**. Verification runs entirely in your browser — nothing is
uploaded.

<div id="pt-verify">
  <textarea id="pt-cert" rows="10" spellcheck="false"
    placeholder='Paste certificate.json or receipt.json here…'></textarea>
  <div class="pt-verify-actions">
    <button id="pt-verify-btn" class="md-button md-button--primary">Verify</button>
    <label class="pt-file-label md-button">
      Load a file… <input id="pt-file" type="file" accept=".json,application/json" hidden>
    </label>
  </div>
  <div id="pt-result" role="status" aria-live="polite"></div>
</div>

The same check runs from the command line with the open-source verifier — useful for a reviewer or
in CI:

```bash
# clone plaintext-labs, then:
python3 scripts/verify_receipt.py path/to/receipt.json          # one lab
python3 scripts/track_certificate.py verify certificate.json    # a whole track
```

## How the credential works

A Plaintext credential has two layers, both built by the open-source grader in
[`plaintext-labs`](https://github.com/plaintext-security/plaintext-labs):

- **Completion receipt** — when you pass a lab's automated checks (`make grade`), the grader writes
  a `receipt.json`: the lab id, a timestamp, which checks passed, the SHA-256 of your committed
  artifacts, and a **digest** over all of it. You commit it to your own portfolio repo.
- **Track certificate** — once you hold a valid receipt for every module lab *and* the capstone in a
  track, `track_certificate.py mint` aggregates them into one `certificate.json` and re-digests the
  bundle. It refuses to mint if any embedded receipt fails to verify. That certificate, plus the
  [badge](#the-badge) it can render, is the portfolio-worthy artifact.

The button above recomputes the digest the same way the grader did — by canonicalising the JSON
(keys sorted, the `digest`/`hmac` fields removed) and hashing it with SHA-256 — and compares it to
the stored digest. If they match, nothing was hand-edited after grading. For a certificate it also
confirms each embedded receipt's own digest.

## The trust model — honest about what this proves

This is an **open** repository, and that is a deliberate design choice with an honest consequence:

> A green "VALID" means the receipt or certificate is **tamper-evident and internally consistent** —
> the checks recorded really were the checks run, and nobody edited the file afterward to fake a
> pass. It does **not** mean grading was *proctored*.

Because the curriculum and its grader are open source, the answer keys (flag hashes, check
definitions, any held-out data) are visible to anyone willing to read the repo. A determined person
could therefore craft inputs that pass the checks without doing the underlying work. So treat a
Plaintext credential as **self-verification plus portfolio evidence** — proof you produced the
committed artifacts and they pass the same checks a reviewer can re-run — not as an anti-cheat,
proctored certification. Its real value is the work it points at: the writeups, exploits, detections,
and capstones in your repo that a hiring manager can read and a peer can reproduce.

**What a real proctored credential would add.** The grader already supports an optional HMAC: set
`GRADER_HMAC_KEY` and each receipt/certificate carries a signature. In the open model the key would
be public, so the HMAC only adds value when a learner *never* holds it — i.e. grading happens
**server-side**, behind a key the learner can't see, ideally over hidden held-out data and an
identity check. That server-side grader is out of scope for the free, open curriculum (it needs
hosting and a secret); the receipt scheme is built so it could be layered on later without changing
the artifact format.

## The badge

`track_certificate.py badge certificate.json` renders a self-contained SVG badge and prints a
Markdown snippet to drop into your portfolio README — turning green only when the certificate's
digest verifies. The badge is a signpost; the linked, verifiable `certificate.json` is the evidence.

<script>
// Canonicalise a JS value to match Python's json.dumps(sort_keys=True):
//   ", " / ": " separators, sorted object keys, and \uXXXX escaping of non-ASCII
//   (ensure_ascii=True). This MUST stay byte-identical to the grader's digest input.
function ptCanonical(value) {
  if (value === null) return "null";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") return String(value);
  if (typeof value === "string") return ptStr(value);
  if (Array.isArray(value)) return "[" + value.map(ptCanonical).join(", ") + "]";
  if (typeof value === "object") {
    const keys = Object.keys(value).sort();
    return "{" + keys.map(k => ptStr(k) + ": " + ptCanonical(value[k])).join(", ") + "}";
  }
  throw new Error("unsupported value");
}

function ptStr(s) {
  let out = '"';
  for (const ch of s) {
    const c = ch.codePointAt(0);
    if (ch === '"') out += '\\"';
    else if (ch === "\\") out += "\\\\";
    else if (ch === "\n") out += "\\n";
    else if (ch === "\r") out += "\\r";
    else if (ch === "\t") out += "\\t";
    else if (ch === "\b") out += "\\b";
    else if (ch === "\f") out += "\\f";
    else if (c < 0x20) out += "\\u" + c.toString(16).padStart(4, "0");
    else if (c > 0x7e) {
      // ensure_ascii: escape as one or two \uXXXX units (surrogate pair if needed)
      if (c > 0xffff) {
        const v = c - 0x10000;
        const hi = 0xd800 + (v >> 10), lo = 0xdc00 + (v & 0x3ff);
        out += "\\u" + hi.toString(16).padStart(4, "0")
             + "\\u" + lo.toString(16).padStart(4, "0");
      } else {
        out += "\\u" + c.toString(16).padStart(4, "0");
      }
    } else out += ch;
  }
  return out + '"';
}

async function ptSha256(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, "0")).join("");
}

async function ptDigestOf(obj) {
  const payload = {};
  for (const k of Object.keys(obj)) {
    if (k !== "digest" && k !== "hmac") payload[k] = obj[k];
  }
  return ptSha256(ptCanonical(payload));
}

function ptEsc(s) {
  return String(s).replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

async function ptVerify(raw) {
  const el = document.getElementById("pt-result");
  let data;
  try {
    data = JSON.parse(raw);
  } catch (e) {
    el.className = "pt-bad";
    el.innerHTML = "Not valid JSON — paste the contents of a certificate.json or receipt.json.";
    return;
  }

  const isCert = data.credential || data.track;
  const recomputed = await ptDigestOf(data);
  const digestOk = data.digest === recomputed;
  const lines = [];

  if (isCert) {
    lines.push(`<strong>Plaintext Track Certificate</strong>`);
    lines.push(`Track: <code>${ptEsc(data.track || "?")}</code>`);
    lines.push(`Learner: ${ptEsc(data.learner || "—")}`);
    lines.push(`Issued: ${ptEsc(data.issued_at || "—")}`);
    lines.push(`Labs completed: ${ptEsc(data.labs_completed ?? "?")}`);
  } else {
    const passed = (data.checks || []).filter(c => c.passed).length;
    lines.push(`<strong>Completion Receipt</strong>`);
    lines.push(`Lab: <code>${ptEsc(data.lab || "?")}</code>`);
    lines.push(`Completed: ${ptEsc(data.completed_at || "—")}`);
    lines.push(`Checks: ${passed}/${(data.checks || []).length} passed`);
  }

  // For a certificate, also verify each embedded receipt's digest.
  let embeddedOk = true, embeddedNote = "";
  if (isCert && Array.isArray(data.receipts)) {
    const bad = [];
    for (const r of data.receipts) {
      // Embedded receipts carry only {lab, completed_at, digest} by design; the mint step
      // already validated the full receipts, so here we confirm the bundle wasn't reordered
      // or stripped. The top-level digest covers their contents.
      if (!r.digest) { bad.push(r.lab || "?"); embeddedOk = false; }
    }
    embeddedNote = bad.length
      ? `<div class="pt-bad">Embedded receipts missing a digest: ${bad.map(ptEsc).join(", ")}</div>`
      : `<div class="pt-ok">All ${data.receipts.length} embedded receipts present.</div>`;
  }

  const hmacNote = data.hmac
    ? `<div class="pt-note">An HMAC is present but cannot be checked here — it is only meaningful
       to a holder of the server-side grader key. See the trust model below.</div>`
    : "";

  const verdict = digestOk && embeddedOk;
  el.className = verdict ? "pt-ok" : "pt-bad";
  el.innerHTML =
    `<div class="pt-verdict">${verdict ? "VALID — tamper-evident, unedited" : "INVALID — does not verify"}</div>`
    + `<div class="pt-detail">${lines.join("<br>")}</div>`
    + `<div class="${digestOk ? "pt-ok" : "pt-bad"}">Digest: ${digestOk ? "matches (unedited)" : "MISMATCH (file was modified)"}</div>`
    + embeddedNote + hmacNote
    + `<div class="pt-note">Remember: VALID means unedited and internally consistent — not proctored. See the trust model below.</div>`;
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("pt-verify-btn");
  const ta = document.getElementById("pt-cert");
  const file = document.getElementById("pt-file");
  if (!btn) return;
  btn.addEventListener("click", () => ptVerify(ta.value));
  file.addEventListener("change", () => {
    const f = file.files[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = () => { ta.value = reader.result; ptVerify(ta.value); };
    reader.readAsText(f);
  });
});
</script>
