# plaintext

> Open security education for everyone. No paywalls. No gatekeeping. Forever free.

Plaintext is a community-built cybersecurity curriculum: hands-on, job-ready, and
AI-augmented, built open-source-first. Professional-grade training from foundations to
advanced specialisations — free to use, free to fork, free to improve.

**Live site:** <https://patrickdaj.github.io/plaintext/> — built with Material for MkDocs
from the Markdown under `tracks/`.

## Tracks

| # | Track | Tools |
|---|-------|-------|
| 00 | [Foundations](tracks/00-foundations/) | tcpdump, openssl, python, bash |
| 01 | [Offensive Security](tracks/01-offensive/) | nmap, metasploit, burpsuite CE, sqlmap |
| 02 | [Defensive Operations](tracks/02-defensive/) | elastic, zeek, suricata, wazuh |
| 03 | [Digital Forensics](tracks/03-forensics/) | autopsy, volatility, wireshark, sleuthkit |
| 04 | [Malware Analysis](tracks/04-malware/) | ghidra, cutter, cuckoo, remnux |
| 05 | [Cloud Security](tracks/05-cloud/) | prowler, pacu, cloudsploit, trivy |

## Structure

```
tracks/                         ← curriculum source (MkDocs builds this into the site)
└── 00-foundations/
    ├── README.md               ← track content map (overview, modules, capstone)
    └── modules/
        └── 01-networking/
            ├── README.md       ← concept explanation
            └── lab.md          ← hands-on, Docker-first exercise
```

## Run it locally

```bash
python3 -m pip install -r requirements.txt
mkdocs serve     # live preview at http://127.0.0.1:8000
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions welcome — fixes,
new modules, translations, lab improvements.

## License

[CC BY 4.0](LICENSE) — use it, share it, build on it.
