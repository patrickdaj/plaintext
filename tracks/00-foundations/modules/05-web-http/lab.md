# Lab 05 — Dissecting HTTP with curl

## Setup
Docker-first — run a local echo server so you can see exactly what you send:
```bash
docker run --rm -d -p 8080:80 --name httpbin kennethreitz/httpbin
```
Then use your host's `curl` against `http://localhost:8080`.

## Scenario
Send requests to a local httpbin instance and read every part of the exchange.

## Do
1. [ ] `curl -v http://localhost:8080/get` — read the full request and response headers.
2. [ ] `curl -X POST http://localhost:8080/post -d 'user=alice&role=admin'` — watch the body echoed back.
3. [ ] `curl -i http://localhost:8080/redirect/1` then `curl -iL http://localhost:8080/redirect/1` — observe a 302, then follow it.
4. [ ] Set a cookie and resend it:
   ```bash
   curl -i 'http://localhost:8080/cookies/set?session=abc123'
   curl --cookie 'session=abc123' http://localhost:8080/cookies
   ```
5. [ ] Clean up: `docker rm -f httpbin`

## Success criteria — you're done when
- [ ] You can identify the method, status code, and key headers in an exchange.
- [ ] You can explain what `Location` does on a redirect.
- [ ] You can describe how the cookie carried state between two otherwise stateless requests.

## Deliverables
`http-notes.md`: an annotated request/response pair, and one sentence on why the server
"trusting" `role=admin` is a problem.

## AI acceleration
Ask a model to explain each response header httpbin returns — then decide for yourself which
are security-relevant versus noise.

## Connects forward
This is the literacy Track 01's web modules (injection, auth, SSRF) and Track 02's web
telemetry assume.

## Marketable proof
> "I can read and craft raw HTTP with curl — methods, headers, status codes, redirects, and
> cookies — which is the basis of every web attack and defense."

## Stretch
- Capture an HTTPS request with `curl -v https://example.com`: you'll see the TLS
  negotiation but not the payload. Tie it back to module 04.
