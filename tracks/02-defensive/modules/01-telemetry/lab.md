# Lab 01 — Stand Up a Log Pipeline

## Setup
Docker-first — a single-node Elasticsearch + Kibana (dev mode):
```bash
docker network create elk
docker run --rm -d --name es --network elk -p 9200:9200 \
  -e discovery.type=single-node -e xpack.security.enabled=false \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.0
docker run --rm -d --name kib --network elk -p 5601:5601 \
  -e ELASTICSEARCH_HOSTS=http://es:9200 docker.elastic.co/kibana/kibana:8.13.0
```
Real data: a real log set from [loghub](https://github.com/logpai/loghub) (e.g. the OpenSSH or
Apache logs), or your own host's syslog/auth log.

## Scenario
Build the searchable log store the rest of the track depends on, and load real logs into it.

## Do
1. [ ] Stand up Elasticsearch + Kibana and confirm both are reachable.
2. [ ] Ingest a real log dataset (a loghub sample, or your own host's auth/syslog).
3. [ ] In Kibana, search the data — find a specific event and filter on a field. (Can you find the
   failed logins?)
4. [ ] Identify one telemetry *gap*: what attacker activity would these logs miss?

## Success criteria — you're done when
- [ ] Real logs are searchable in Kibana.
- [ ] You can find a specific event and filter by a field.
- [ ] You can name one thing this telemetry would not catch.

## Deliverables
`telemetry.md`: what you ingested, a couple of useful searches, and the gap you identified.

## AI acceleration
Have a model draft the ingest/parse config — then verify the fields actually land correctly in the
index. A mis-parsed log is invisible to every later detection.

## Connects forward
This pipeline is the substrate for every later Defensive module — detections (08), hunting (11–12),
and response (13–15) all query it.

## Marketable proof
> "I stand up a central log pipeline (Elastic) and ingest real telemetry — and I reason about
> collection gaps before writing a single detection."

## Automate & own it
**Required.** Capture the whole pipeline as a `docker-compose` + ingest config that stands up from
zero and loads the data; AI drafts it, you verify what lands in the index; commit it.

## Stretch
- Add a second log source (network, or a second host) and normalise both into a common field set
  (a preview of module 07).
