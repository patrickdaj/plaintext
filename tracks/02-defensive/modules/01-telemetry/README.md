# Module 01 — Telemetry & Log Centralisation

**Defensive Operations** — *you can't detect what you don't collect; this is the data plane everything else runs on.*

## Why this matters
Detection, hunting, and response all start with data. Before you can write a single detection you
need the right telemetry — host, network, identity — shipped reliably into one searchable place.
Getting collection right (and complete) is the unglamorous foundation that decides whether you can
see an attacker at all. This module builds that pipeline.

## Objective
Stand up a central log store, ship real log data into it, and reason about what telemetry actually
matters for detection.

## Learn (~4 hrs)

**The data plane**
- [Elastic Stack — Create a Free SIEM (video, part 1)](https://www.youtube.com/watch?v=GvzosoaOaIQ) — a hands-on build of Elasticsearch + Kibana as a SIEM.
- [Elastic — Elasticsearch & Kibana docs](https://www.elastic.co/guide/index.html) — the reference; read the "Getting Started" for ingest, index, and search.

**What to collect**
- [MITRE ATT&CK — Data Sources](https://attack.mitre.org/datasources/) — what telemetry maps to which techniques, so you collect with detection in mind.

## Key concepts
- Log sources: host, network, identity, cloud
- Shippers/agents (fluent-bit, vector, beats)
- Centralisation and indexing
- What "good" telemetry looks like — and the gaps that blind you
- Retention and volume tradeoffs

## AI acceleration
A model drafts your shipper config and an ingest pipeline in seconds — and just as easily produces
one that silently drops fields or mis-parses timestamps. Verify what actually lands in the index,
not what the config claims.
