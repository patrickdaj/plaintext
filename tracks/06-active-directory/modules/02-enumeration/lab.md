# Lab 02 — Enumerate the Meridian Domain

*Hands-on lab · [← Back to the module concept](README.md)*


## Setup

This is a **reference lab** — the environment lives in the companion repo:

```bash
git clone https://github.com/plaintext-security/plaintext-labs
cd plaintext-labs/active-directory/02-enumeration
make up      # start Samba4 DC + attacker container (~2 min first build)
make demo    # run automated ldapsearch enumeration queries
make shell   # drop into the attacker container to run your own queries
make down    # stop everything when done
```

The lab provides:
- `samba-dc` — a Samba4 container acting as `dc01.meridian.local` with 30+ pre-seeded users and all the misconfigurations from `data/meridian-domain.md`.
- `attacker` — a Debian container with `ldapsearch`, `enum4linux-ng`, and `bloodhound-python` installed, pre-configured to reach the DC.
- `data/bloodhound-meridian.json` — a pre-generated BloodHound dataset for the Meridian domain (import this into BloodHound CE if you want the graph without running the full ingestor).

> Only attack environments you own or have explicit written permission to test.

## Scenario

You're a red teamer who has just obtained credentials for `jsmith` (password: `Welcome1!`) on the Meridian Financial network. Your goal is to enumerate the entire domain — users, groups, service accounts, SPNs, and delegation settings — and build a BloodHound graph that shows the attack paths available from `jsmith`.

## Do

1. [ ] **Baseline with enum4linux-ng.** From the attacker container, run:
   ```
   enum4linux-ng -A -u jsmith -p 'Welcome1!' dc01.meridian.local
   ```
   Note what the tool discovers without you writing a single LDAP filter. How many users, groups, and shares does it find? What would it have found if you'd run it *without* `-u` / `-p` (null session)?

2. [ ] **Raw LDAP — user enumeration.** Run an ldapsearch to list all user accounts in the domain:
   ```
   ldapsearch -H ldap://dc01.meridian.local -x -D 'jsmith@MERIDIAN.LOCAL' -w 'Welcome1!' \
     -b 'DC=meridian,DC=local' '(objectClass=user)' sAMAccountName userPrincipalName memberOf
   ```
   Save the output. Count the accounts. Which ones do not appear to be human users?

3. [ ] **Find Kerberoastable accounts.** Modify the filter to return only accounts with a `servicePrincipalName`:
   ```
   ldapsearch ... '(&(objectClass=user)(servicePrincipalName=*))' sAMAccountName servicePrincipalName
   ```
   List the SPNs you find. Cross-reference with `data/meridian-domain.md` — did you find all three Kerberoastable accounts?

4. [ ] **Find AS-REP roastable accounts.** Filter for `userAccountControl` flag `4194304` (DONT_REQUIRE_PREAUTH):
   ```
   ldapsearch ... '(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))' sAMAccountName
   ```
   Which accounts have this flag set? Why is this dangerous without any password at all?

5. [ ] **Find unconstrained delegation.** Query for computers and accounts with unconstrained delegation (`userAccountControl` flag `524288`):
   ```
   ldapsearch ... '(userAccountControl:1.2.840.113556.1.4.803:=524288)' sAMAccountName
   ```
   Note which accounts appear. Why does this list always include DCs?

6. [ ] **Run bloodhound-python.** Collect full BloodHound data from the DC:
   ```
   bloodhound-python -d MERIDIAN.LOCAL -u jsmith -p 'Welcome1!' -c All -ns 10.10.0.10 --zip
   ```
   This generates a ZIP file. Import it into BloodHound CE (run externally at `http://localhost:8080` if you have it), or examine the raw JSON files inside the ZIP.

7. [ ] **Analyse the BloodHound data.** Whether using the CE UI or the raw JSON, answer: what is the shortest path from `jsmith` to `Domain Admins`? How many hops? List each hop and the edge type (e.g., `MemberOf`, `GenericWrite`, `CanPSRemote`).

   Alternatively, import `data/bloodhound-meridian.json` into BloodHound CE to see a pre-generated graph.

## Success criteria — you're done when

- [ ] You have a complete list of Meridian users, groups, and computers from ldapsearch.
- [ ] You have identified all three Kerberoastable SPNs and both AS-REP roastable accounts.
- [ ] You have identified the unconstrained delegation accounts.
- [ ] You have a BloodHound dataset (generated or from `data/`) imported and can answer "shortest path from jsmith to DA" with specific hops and edge types.
- [ ] You have written down what a defender would see in DC event logs for each query you ran.

## Deliverables

`enumeration-report.md` — a structured list of findings: users/groups/SPNs/delegation flags discovered, the shortest path to DA with edge types, and your notes on detection opportunities. Commit it.

## Automate & own it

**Required.** Write `enumerate.py` — a Python script using `ldap3` (or subprocess + ldapsearch) that queries the DC, collects all users with SPNs, all users without pre-auth, and all accounts with unconstrained delegation, and prints a clean summary. Have a model draft it; you verify the LDAP filter strings match what you ran manually and confirm the output against your ldapsearch results. Commit the script next to your report.

## AI acceleration

Paste the raw BloodHound JSON for a node into a model and ask it to explain the attack paths in plain English. It's good at translating graph data into narrative — but you must verify each edge type exists in BloodHound's schema (e.g., `GenericWrite` is real; some model-invented edges are not). The BloodHound GitHub has the canonical edge type list.

## Connects forward

The Kerberoastable SPNs you found here are the targets in module 03. The ACL edges in BloodHound (`GenericWrite`, `WriteDacl`) are the abuse paths in module 05. The full BloodHound dataset is the basis for the path analysis in module 08.

## Marketable proof

> "I enumerate Active Directory environments from a standard domain credential — LDAP, RPC, BloodHound — and produce a structured attack-surface map including privilege paths, Kerberoasting targets, and delegation risks."

## Stretch

- Write a Cypher query (paste into BloodHound CE's raw query interface) that finds all users with `GenericWrite` on a group, and all groups that have `AdminTo` rights on at least one computer. Interpret what each result means for an attacker.
- Research `ldap-monitor` or `ldapdomaindump` as alternative enumeration tools and note what each surfaces differently from ldapsearch.
