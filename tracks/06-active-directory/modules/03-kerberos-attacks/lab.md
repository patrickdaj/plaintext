# Lab 03 — Kerberoasting & AS-REP Roasting

*Hands-on lab · [← Back to the module concept](README.md)*


## Setup

```bash
git clone https://github.com/plaintext-security/plaintext-labs
cd plaintext-labs/active-directory/03-kerberos-attacks
make up      # start Samba4 DC + impacket attacker container (~2 min first build)
make demo    # run Kerberoast + AS-REP roast, display hashes
make shell   # interactive impacket shell
make down    # stop when done
```

The `data/hashes.txt` file contains pre-generated Kerberoast ticket hashes for offline cracking practice — use these if you want to skip straight to hashcat.

> Only attack environments you own or have explicit written permission to test. Never run these techniques against a network you do not control.

## Scenario

As `jsmith` on the Meridian Financial network, you have enumerated the domain (module 02) and identified three Kerberoastable service accounts and two AS-REP roastable accounts. Your goal is to extract their ticket hashes and crack the weakest ones offline. A cracked service account password is the next step in the chain toward Domain Admin.

## Do

1. [ ] **Kerberoast all SPNs.** From the attacker container, run:
   ```
   GetUserSPNs.py MERIDIAN.LOCAL/jsmith:'Welcome1!' -dc-ip 10.10.0.10 -request
   ```
   You should receive hashes for `svc-mssql`, `svc-backup`, and `svc-web`. Save the output to `spn-hashes.txt`. Notice the hash format: `$krb5tgs$23$*...` — the `23` is the etype (RC4).

2. [ ] **Inspect the hash structure.** Open `spn-hashes.txt` and identify: which field contains the account name? Which contains the encrypted ticket blob? Why does the etype matter for cracking speed?

3. [ ] **AS-REP roast.** Run — *with no password at all*:
   ```
   GetNPUsers.py MERIDIAN.LOCAL/ -dc-ip 10.10.0.10 -no-pass -usersfile /data/userlist.txt
   ```
   You should receive AS-REP hashes for `svc-legacy` and `svc-monitor`. The `$krb5asrep$23$` prefix identifies these. Note that no credential was required.

4. [ ] **Crack the hashes offline.** Use hashcat against the sample hashes in `data/hashes.txt`:
   ```
   hashcat -m 13100 data/hashes.txt /usr/share/wordlists/rockyou.txt --force
   ```
   Which account's password cracks? How long did it take? What does this tell you about the password quality of service accounts?

5. [ ] **Understand the etype downgrade.** Re-run the Kerberoast but force AES256:
   ```
   GetUserSPNs.py MERIDIAN.LOCAL/jsmith:'Welcome1!' -dc-ip 10.10.0.10 -request -etype 18
   ```
   Compare the hash prefix (`$krb5tgs$18$` vs `$krb5tgs$23$`). Look up the hashcat mode for AES256 TGS (`-m 19600`). Why does AES make cracking dramatically harder?

6. [ ] **Map to ATT&CK.** Write down: which technique ID covers Kerberoasting? Which covers AS-REP roasting? For each, name the specific detection note from the ATT&CK page (Windows Event ID and what field to filter on).

## Success criteria — you're done when

- [ ] You have extracted Kerberoast hashes for all three SPNs and AS-REP hashes for both no-preauth accounts.
- [ ] At least one hash has been cracked with hashcat (or confirmed crackable using `data/hashes.txt`).
- [ ] You can explain why the attack leaves no lockout events.
- [ ] You have the ATT&CK technique IDs (T1558.003, T1558.004) and the specific Event ID that detects each.

## Deliverables

`kerberoast-report.md` — SPNs found, hashes extracted (truncated, not full — never commit full hashes), cracked accounts (by username and note about password weakness), ATT&CK mapping, and detection notes. Commit the report and your annotated `spn-hashes.txt` (with the hash blobs redacted to the first 20 chars).

## Automate & own it

**Required.** Write `kerberoast-scan.py` — a script that connects to the DC via impacket (use `GetUserSPNs`'s library functions, or shell out), extracts all SPNs, and outputs a summary: account name, SPN, password last set, etype. Have a model draft the impacket calls; you verify each API call against impacket's examples and confirm the output. This becomes a reusable domain health check. Commit it.

## AI acceleration

Ask a model: "Given a Kerberoast hash with etype 23 (RC4), estimate how many hashes per second hashcat achieves on a modern GPU and how long it would take to exhaust rockyou.txt." Then ask it the same for etype 18 (AES256). Use these estimates to explain to a client why migrating service accounts to gMSAs (which have 120-char random passwords) eliminates Kerberoasting entirely.

## Connects forward

The cracked `svc-mssql` or `svc-backup` credential is used for pass-the-hash in module 04. The `svc-backup` unconstrained delegation is abused in module 07 (persistence). Detection of Event 4769 with RC4 etype is the basis for the Sigma rule in module 09.

## Marketable proof

> "I execute Kerberoasting and AS-REP roasting against Active Directory, recover offline-crackable ticket hashes, and explain both the attack mechanics and the specific audit configuration required to detect it."

## Stretch

- Try requesting a TGS for a service account that *does* require AES — is there a way to force RC4 that the KDC allows? Research the `msds-SupportedEncryptionTypes` attribute and what setting forces AES-only.
- Write a Cypher query in BloodHound CE that marks all Kerberoastable accounts (has SPN + not in Protected Users + password age > 1 year) — this is what a real attack-path analysis surfaces automatically.
