# Track 05 — Cloud & Container Security

**Attack and defend cloud-native environments,** and express security as code — because in
the cloud the infrastructure *is* code. AWS/GCP/Azure plus containers and Kubernetes.

## What you'll be able to do
- Reason about shared responsibility, cloud identity, and trust.
- Find and explain privilege-escalation paths through IAM.
- Audit posture and infrastructure-as-code for misconfigurations, gated in CI.
- Secure containers and Kubernetes, and detect and respond to cloud attacks.

## Modules

| # | Module | What you'll learn | OSS tools |
|---|--------|-------------------|-----------|
| 01 | Cloud Fundamentals & Shared Responsibility | The model, accounts, and CLIs | cloud CLIs |
| 02 | Cloud Identity & IAM | Policies, roles, trust, and federation | `cloudfox` |
| 03 | IAM Attack Paths | Finding privilege-escalation chains | `pmapper`, `cloudfox` |
| 04 | Posture & Misconfiguration Auditing | Benchmarking accounts against known issues | `prowler`, `scoutsuite` |
| 05 | Infrastructure-as-Code Security | Scanning Terraform before it deploys | `checkov`, `tfsec`, `trivy` |
| 06 | CI/CD Pipeline Security | Securing the path from commit to deploy | `trivy`, `gitleaks` |
| 07 | Secrets Management & Detection | Storing and finding leaked credentials | `vault`, `trufflehog` |
| 08 | Container & Image Security | Image hygiene and supply-chain scanning | `trivy`, `grype` |
| 09 | Container Escape & Runtime | Breakouts and runtime visibility | `falco` |
| 10 | Kubernetes — RBAC & Network Policy | Least privilege and segmentation as code | `kube-bench` |
| 11 | Kubernetes — Admission & Runtime | Policy enforcement and runtime detection | `kyverno`, `falco` |
| 12 | Cloud Attack Techniques | Exploiting misconfig; simulating safely | `pacu`, `stratus-red-team` |
| 13 | Cloud Logging & Detection | Detecting attacks from cloud trails | `falco`, `sigma` |
| 14 | Cloud Incident Response | Investigating and containing in the cloud | `cloudtrail`, `hayabusa` |

## Prerequisites
Complete Track 00 — Foundations first.

> Labs use your own free-tier accounts or intentionally vulnerable environments (CloudGoat,
> flaws.cloud). Never test accounts or tenants you don't own, and tear down billable
> resources when done.

## Capstone
Find a privilege-escalation path in a deliberately vulnerable cloud account (CloudGoat or
flaws.cloud), explain it, then close it as code — Terraform gated by a scanner in CI — and
detect the attack from cloud logs. **Deliverable:** the attack path, the fix-as-code, and
the detection.

## AI & automation
In the cloud the infrastructure *is* code, and increasingly that code is AI-written —
exactly where misconfigurations hide (over-broad IAM, `0.0.0.0/0`, privileged containers).
The posture this track drills: **AI authors → you review → scanners gate → you own it.**

## Standards & further reading
- CIS Benchmarks for AWS/GCP/Azure and Kubernetes
- MITRE ATT&CK for Cloud and Containers
- Cloud provider Well-Architected / security best-practice guidance
- OWASP Kubernetes and Cloud-Native security guidance
