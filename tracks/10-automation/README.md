# Track 10 — Security Automation

**Automate the pipeline, not just the script.** Infrastructure as code, CI/CD security
gates, and SOAR — the standing automation discipline that runs through every other track,
done deliberately. *Anyone can automate now; doing it well, and owning the result, is the
skill.*

## What you'll be able to do
- Define and review infrastructure as code, with security gated in CI.
- Manage configuration and hardening at scale.
- Build response playbooks that enrich, contain, and ticket with a human in the loop.
- Treat detections and remediation as code.

## Modules

| # | Module | What you'll learn | OSS tools |
|---|--------|-------------------|-----------|
| 01 | The Automation Mindset | Where automation pays off — and where it bites | — |
| 02 | Infrastructure as Code | Reproducible infra from zero | `terraform`, `opentofu` |
| 03 | IaC Security Scanning | Gating misconfigurations in CI | `checkov`, `tfsec` |
| 04 | Configuration Management | Hardening and state at scale | `ansible` |
| 05 | CI/CD Pipelines & Gates | Security checks from commit to deploy | `github actions`, `gitleaks` |
| 06 | Containerising Tooling | Reproducible, shareable security tools | `docker` |
| 07 | Enrichment & Data Pipelines | Scheduled collection and processing | `python`, `cron` |
| 08 | SOAR Fundamentals | Playbooks: enrich → contain → ticket | `Shuffle`, `n8n` |
| 09 | Detection-as-Code Pipelines | Versioned, tested detections in CI | `sigma`, `pytest` |
| 10 | Reviewing AI-Generated Automation | Catching what the model got wrong | `checkov` |

## Prerequisites
Complete Track 00 — Foundations; Track 09 — Python helps.

> Run automation against your own accounts and lab infrastructure only. Generated IaC can
> create real, billable, internet-facing resources — review before you apply.

## Capstone
Build a pipeline that gates a misconfiguration before deploy *and* a SOAR playbook that
responds to an alert with a human approval step — both as reviewed, version-controlled
code. **Deliverable:** the pipeline, the playbook, and a note on what AI generated vs. what
you corrected.

## AI & automation
The whole track *is* the AI/automation thesis: AI writes the YAML, HCL, and playbook
logic — and generated automation is *exactly* where misconfigurations hide (over-broad
RBAC, wildcard IAM, missing approval gates). The posture: **AI authors → you review →
scanners gate → you own it.** "I don't write the YAML, I own the YAML."

## Standards & further reading
- Terraform / OpenTofu and Ansible documentation
- CIS Benchmarks as policy targets
- NIST SP 800-128 (Security Configuration Management)
- MITRE ATT&CK for mapping SOAR responses
