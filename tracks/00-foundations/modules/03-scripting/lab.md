# Lab 03 — A Failed-Login Parser in Python

## Setup
Docker-first (mounts the current directory so your script persists):
```bash
docker run --rm -it -v "$PWD":/work -w /work python:3.12-slim bash
```

## Scenario
Build a tool that reads an auth log and reports the top source IPs by failed-login count —
the triage script you'll write a hundred variations of.

## Do
1. [ ] Create a sample `auth.log`:
   ```
   Jan 1 10:00:01 host sshd[1]: Failed password for root from 10.0.0.9 port 22 ssh2
   Jan 1 10:00:02 host sshd[2]: Failed password for invalid user admin from 10.0.0.5 port 22 ssh2
   Jan 1 10:00:03 host sshd[3]: Failed password for root from 10.0.0.9 port 22 ssh2
   ```
2. [ ] Write `topips.py`:
   ```python
   import re, sys
   from collections import Counter

   PATTERN = re.compile(r"Failed password .* from (\d+\.\d+\.\d+\.\d+)")

   def top_ips(path, n=5):
       counts = Counter()
       with open(path) as f:
           for line in f:
               m = PATTERN.search(line)
               if m:
                   counts[m.group(1)] += 1
       return counts.most_common(n)

   if __name__ == "__main__":
       for ip, count in top_ips(sys.argv[1]):
           print(f"{count:>4}  {ip}")
   ```
3. [ ] Run it: `python3 topips.py auth.log`
4. [ ] Break it on purpose: feed it a malformed line and see how it behaves.

## Success criteria — you're done when
- [ ] The script prints a ranked count of source IPs from the sample.
- [ ] It does something sensible (doesn't crash) on a line it can't parse.
- [ ] You can explain every token in the regex.

## Deliverables
`topips.py` plus a one-paragraph README: what it does, how to run it, and one limitation
you'd fix next.

## AI acceleration
Have a model extend it to emit JSON or flag IPs over a threshold — then review the regex
and edge cases (IPv6? malformed lines?) before you trust the output.

## Connects forward
This is the on-ramp to Track 09 (Python for Security) and the parsing habit Track 02
(detection engineering) runs on.

## Marketable proof
> "I automate triage in Python — log parsing, enrichment, ranked output — and I can review
> and harden AI-generated tooling instead of pasting it blind."

## Stretch
- Add `--json` and `--threshold N` flags with `argparse`, and let it read from stdin too.
