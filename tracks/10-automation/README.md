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
| 01 | [The Automation Mindset](modules/01-automation-mindset/README.md) | Where automation pays off — and where it bites | — |
| 02 | [Infrastructure as Code](modules/02-infrastructure-as-code/README.md) | Reproducible infra from zero | `terraform`, `opentofu` |
| 03 | [IaC Security Scanning](modules/03-iac-security-scanning/README.md) | Gating misconfigurations in CI | `checkov`, `tfsec` |
| 04 | [Configuration Management](modules/04-configuration-management/README.md) | Hardening and state at scale | `ansible` |
| 05 | [CI/CD Pipelines & Gates](modules/05-cicd-pipelines/README.md) | Security checks from commit to deploy | `github actions`, `gitleaks` |
| 06 | [Containerising Tooling](modules/06-containerising-tooling/README.md) | Reproducible, shareable security tools | `docker` |
| 07 | [Enrichment & Data Pipelines](modules/07-enrichment-pipelines/README.md) | Scheduled collection and processing | `python`, `cron` |
| 08 | [SOAR Fundamentals](modules/08-soar-fundamentals/README.md) | Playbooks: enrich → contain → ticket | `Shuffle`, `n8n` |
| 09 | [Detection-as-Code Pipelines](modules/09-detection-as-code-pipelines/README.md) | Versioned, tested detections in CI | `sigma`, `pytest` |
| 10 | [Reviewing AI-Generated Automation](modules/10-reviewing-ai-automation/README.md) | Catching what the model got wrong | `checkov` |

## Phases & projects

The ten modules run in three phases; each ends in a **project** that integrates its modules (a phase
is the substantial, standalone unit — a single module is a few hours). Every project is reviewed,
version-controlled code with a note on what AI generated vs. what you corrected.

- **Phase 1 · Infrastructure & config as code** (01–04) — **Project:** define a small environment in
  Terraform/OpenTofu and configure it with Ansible, with `checkov`/`tfsec` gating misconfigurations —
  proving a deliberately over-broad rule is *blocked* before apply.
- **Phase 2 · Pipelines & portable tooling** (05–07) — **Project:** a CI/CD pipeline that runs
  secret-scanning and security gates from commit to deploy, a containerised security tool that runs
  the same everywhere, and a scheduled enrichment pipeline feeding processed data downstream.
- **Phase 3 · Response & detection as code** (08–10) — **Project:** the track capstone — a SOAR
  playbook that enriches → contains → tickets with a human approval step, plus detections-as-code
  tested in CI — and a review pass that catches what an AI-generated version got wrong.

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
