# Lab 05 — Browser & Application Artifacts

*Hands-on lab · [← Back to the module concept](README.md)*


## Setup
This is a **reference lab** — its environment lives in the companion
[`plaintext-labs`](https://github.com/plaintext-security/plaintext-labs) repo:

```bash
git clone https://github.com/plaintext-security/plaintext-labs
cd plaintext-labs/forensics/05-browser-app-artifacts
make up        # build the hindsight + sqlite3 container
make demo      # extract and display browser artifacts from the seed History file
make shell     # drop in to work interactively
make down      # stop when done
```

The container includes `hindsight` and `sqlite3`. `data/History` is a small SQLite Chrome
history database with planted Meridian-scenario browsing data.

> Everything runs against a bundled SQLite file you own. No authorization needed.

## Scenario
During the Meridian IR, the analyst imaged the compromised user's Chrome profile directory before shutdown. The `History` file was extracted and handed to you. The finance user (`svc_batch_finance`) claims they only used the browser for "normal work." Your task is to **reconstruct the browser activity** during the incident window and determine whether the browser evidence supports or contradicts that claim.

> Only examine browser artifacts from systems you are authorised to investigate. In a real case, these files arrive via the forensically acquired disk image from Module 02.

## Do

1. [ ] **Run hindsight against the History file.**
   ```bash
   hindsight.py -i data/ -o /tmp/hindsight-output -f xlsx
   ```
   Open the XLSX (or run with `-f jsonl` and `cat` the output). What does hindsight report for:
   - Total URLs visited
   - Date range of the history
   - Top visited domains

2. [ ] **Query visited URLs directly with sqlite3.**
   ```bash
   sqlite3 data/History \
     "SELECT datetime(last_visit_time/1000000 - 11644473600, 'unixepoch') as visited_at,
             url, visit_count, title
      FROM urls ORDER BY last_visit_time DESC LIMIT 20;"
   ```
   Which URLs were visited during the incident window (2024-03-15 02:00–02:35 UTC)?
   Note any cloud storage, webmail, or file-sharing domains.

3. [ ] **Examine the downloads table.**
   ```bash
   sqlite3 data/History \
     "SELECT datetime(start_time/1000000 - 11644473600, 'unixepoch') as downloaded_at,
             target_path, tab_url, total_bytes, state
      FROM downloads ORDER BY start_time DESC;"
   ```
   What was downloaded? From where? Does the download URL align with the exfiltration narrative?

4. [ ] **Extract search terms.**
   ```bash
   sqlite3 data/History \
     "SELECT datetime(u.last_visit_time/1000000 - 11644473600, 'unixepoch') as searched_at,
             k.term, u.url
      FROM keyword_search_terms k JOIN urls u ON k.url_id = u.id
      ORDER BY u.last_visit_time DESC;"
   ```
   What search terms appear? Do any suggest the user was looking for exfiltration methods, external file storage, or ways to cover tracks?

5. [ ] **Check the WAL file.**
   The `data/History-wal` (if present) may contain rows from after a history clear. Use `sqlite3` to see if the WAL has any data:
   ```bash
   sqlite3 data/History "PRAGMA wal_checkpoint(FULL);" && \
   sqlite3 data/History "SELECT count(*) FROM urls;"
   ```
   Does the row count change after a checkpoint? This demonstrates why clearing browser history doesn't necessarily wipe the WAL.

6. [ ] **Write your findings.**
   Produce `browser-findings.md` with:
   - Timeline of browser activity during the incident window (2024-03-15 02:00–02:35)
   - Downloads found and their source URLs
   - Search terms that are relevant to the investigation
   - Assessment: does the browser history support or contradict the user's claim of "normal work"?
   - Short paragraph on what private/incognito mode would and wouldn't have hidden in this scenario.

## Success criteria — you're done when
- [ ] hindsight has been run and its output reviewed.
- [ ] At least 5 URLs from the incident window are documented with timestamps.
- [ ] Downloads table was queried and findings documented.
- [ ] Search terms were extracted and assessed for relevance.
- [ ] `browser-findings.md` includes a clear assessment of the user's claim.

## Deliverables
Commit `browser-findings.md` to your fork. Do not commit `/tmp/hindsight-output/` or any modified copies of the `History` file.

## Automate & own it
**Required.** Write a Python script `browser-triage.py` that:
1. Takes a path to a Chrome `History` SQLite file and a time window (start, end) as arguments.
2. Queries and outputs: URLs visited in the window, downloads, and search terms.
3. Formats the output as a Markdown table.
4. Flags any URLs matching a list of known file-sharing or exfiltration-risk domains (e.g., `mega.nz`, `wetransfer.com`, `dropbox.com`, `drive.google.com`).

Have a model draft the script; **read every line** including the timestamp conversion — that's the most error-prone part. Test it against `data/History` and verify at least one timestamp against the hindsight output before committing.

## AI acceleration
Feed the browser history output to a model and ask it to identify which domains are high-risk for data exfiltration in a corporate context. Ask it to explain the Chrome timestamp epoch conversion and generate a SQL query for a specific time window. Verify every timestamp it produces by checking a known reference visit against the SQL output — the epoch conversion is the most common source of error.

## Connects forward
Browser artifacts feed the super-timeline in Module 07 (plaso parses Chrome history natively and merges it with EVTX and filesystem events). The download records connect to Module 06 (if a malicious payload was downloaded, the memory forensics module will show it running).

## Marketable proof
> "I extract and correlate browser artifacts — history, downloads, search terms, and WAL data — using hindsight and direct SQLite queries, and I can tell you whether a user's claimed activity matches what the browser actually recorded."

## Stretch
- Research how Firefox stores its history (it's also SQLite, but the schema differs). Write a Python snippet to query `places.sqlite` for the same fields you extracted from Chrome.
- Look up what incognito mode *does* preserve: DNS cache (OS-level), network flow data, proxy logs. Sketch a scenario where you could partially reconstruct incognito browsing from non-browser sources.
