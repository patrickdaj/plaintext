# Lab 09 — Detect AD Attacks with Sigma and Chainsaw

*Hands-on lab · [← Back to the module concept](README.md)*


## Setup

```bash
git clone https://github.com/plaintext-security/plaintext-labs
cd plaintext-labs/active-directory/09-detecting-ad-attacks
make up      # start the chainsaw container with EVTX data + Sigma rules
make demo    # run chainsaw over all EVTX files with the bundled Sigma rules
make shell   # interactive shell to write and test your own rules
make down
```

The `data/evtx/` directory contains real-shaped EVTX files for each AD attack:
- `kerberoast-4769.evtx` — Event 4769 with RC4 etype (Kerberoast)
- `asrep-4768.evtx` — Event 4768 with PreAuthType=0 (AS-REP roast)
- `dcsync-4662.evtx` — Event 4662 with DS-Replication (DCSync)
- `pth-4624.evtx` — Event 4624 Type 3 with NtLmSsp (PTH)

The `data/rules/` directory contains three pre-written Sigma rules for you to study and extend.

> This lab analyses bundled EVTX data. No live attack systems involved.

## Scenario

You are a detection engineer at Meridian Financial. The red team has finished their engagement and handed you the attack timeline. Your job: write Sigma rules that would have detected each step of the attack path from module 08, validate them against the bundled EVTX samples with chainsaw, and ensure each rule has the correct ATT&CK tag and the right audit policy requirement documented.

## Do

1. [ ] **Run the demo.** `make demo` runs chainsaw over all EVTX files using the bundled rules. Read the output — which rules fired? What fields did chainsaw surface in the match? Note the event record ID and timestamp.

2. [ ] **Study the Kerberoast rule.** Open `data/rules/kerberoast.yml`. Understand each field:
   - `logsource`: why is `category: kerberos` + Windows Security important?
   - `detection.selection`: what specific field and value catches Kerberoasting?
   - `tags`: confirm the ATT&CK technique ID is T1558.003.
   Validate it manually: open `data/evtx/kerberoast-4769.evtx` in the shell with `chainsaw search --json -e 4769 kerberoast-4769.evtx | head -50` — does the EncryptionType field in the event match the rule filter?

3. [ ] **Write the DCSync Sigma rule.** The `data/rules/` directory includes a stub (`dcsync-stub.yml`). Fill it in:
   - EventID: 4662
   - ObjectType: DS-Replication-Get-Changes-All (GUID: `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2`)
   - SubjectUserName: must NOT end in `$` (exclude machine accounts / DCs)
   - ATT&CK tag: T1003.006
   Validate with: `chainsaw hunt data/evtx/dcsync-4662.evtx -s data/rules/dcsync.yml --mapping data/sigma-mappings.yml`

4. [ ] **Write the PTH Sigma rule.** Create `data/rules/pth.yml`:
   - EventID: 4624
   - LogonType: 3
   - AuthenticationPackageName: `NTLM`
   - SubjectUserSid: NOT `S-1-0-0` (null SID)
   - WorkstationName: not null (source workstation present)
   - Filter: exclude machine accounts (TargetUserName ending in `$`), exclude localhost
   Validate against `data/evtx/pth-4624.evtx`.

5. [ ] **Test false-positive behaviour.** The `data/evtx/` directory also contains `baseline-4624.evtx` — normal domain logon events. Run your PTH rule against it. Do any events match? If so, what would you add to the filter to suppress them?

6. [ ] **Document the audit policy requirement.** For each of the four rules, write down which specific audit category must be enabled on the DC for the event to appear at all. This is the prerequisite that most environments miss.

## Success criteria — you're done when

- [ ] All four Sigma rules (kerberoast, AS-REP, DCSync, PTH) fire on their respective EVTX files.
- [ ] None of the four rules fire on `baseline-4624.evtx` with more than 2 false positives.
- [ ] Each rule is tagged with the correct ATT&CK technique.
- [ ] You have documented the required audit policy for each rule.

## Deliverables

`data/rules/kerberoast.yml`, `dcsync.yml`, `asrep.yml`, `pth.yml` — the four Sigma rules. Commit them. Also commit `detection-report.md` — the audit policy requirements for each rule, your false-positive analysis, and the chainsaw output showing the rules firing.

## Automate & own it

**Required.** Add a CI check: a GitHub Actions workflow (`.github/workflows/validate-rules.yml`) that runs chainsaw over the EVTX samples with each Sigma rule and fails if any rule doesn't produce at least one match on its target EVTX file. Have a model draft the workflow; you verify the chainsaw command syntax and the failure condition. This is detection-as-code CI: a rule that doesn't catch the attack can't merge. Commit it.

## AI acceleration

After writing each rule, paste it into a model and ask: "What false positive scenarios could cause this rule to fire on benign activity?" The model is good at enumerating FP scenarios for well-known Windows events. Use its list to add filter conditions to your rule, then re-run chainsaw against the baseline EVTX to confirm the FPs are suppressed.

## Connects forward

These Sigma rules are the detection layer for the hardening controls in module 10. The audit policy requirements you documented are part of the hardening checklist. Module 11 covers integrating these detections into a continuous monitoring architecture.

## Marketable proof

> "I write Sigma detections for Active Directory attacks — Kerberoasting, DCSync, pass-the-hash — validate them against real EVTX telemetry with chainsaw, and wire them into CI so broken detections can't merge."

## Stretch

- Write a honeytoken detection: a Sigma rule that fires on any Event 4769 for a specific honeytoken SPN (`HoneyToken/fake.meridian.local`). By definition, any match is attacker activity. How does this compare in alert reliability to the rate-based Kerberoasting detection?
- Research **Wazuh** integration: how would you push these Sigma rules into Wazuh's ruleset? What is the conversion path from Sigma YAML to Wazuh XML rule format?
