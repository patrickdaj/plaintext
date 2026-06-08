# Lab 01 — Capture and Dissect a Live Exchange

## Setup
Docker-first — `netshoot` ships every tool you need (`tcpdump`, `curl`, `dig`):
```bash
docker run --rm -it nicolaka/netshoot bash
```

## Scenario
Observe one HTTP request end to end — the DNS lookup and the TCP handshake — captured by
you and read by you.

> Capture only on systems/networks you own, or inside this throwaway container.

## Do
1. [ ] Start a capture in the background: `tcpdump -i any -w cap.pcap &`
2. [ ] Generate traffic: `dig example.com` then `curl http://example.com`
3. [ ] Stop the capture: `kill %1`
4. [ ] Read the DNS exchange: `tcpdump -r cap.pcap -n port 53`
5. [ ] Isolate the handshake: `tcpdump -r cap.pcap -n 'tcp[tcpflags] & (tcp-syn|tcp-ack) != 0'`
6. [ ] (Optional) Copy `cap.pcap` to your host, open it in Wireshark, and "Follow TCP Stream."

## Success criteria — you're done when
- [ ] You can point to the DNS query and the A record it returned.
- [ ] You can identify the SYN, SYN-ACK, and ACK that open the connection.
- [ ] You can state the client and server ports and the order of the first ~6 packets.

## Deliverables
A short `networking.md`: the resolved IP, the annotated handshake packets, and how many
packets were exchanged before any data flowed. Reference `cap.pcap` — do **not** commit it
(see `.gitignore`).

## AI acceleration
Paste any `tcpdump` line you don't understand to a model for a plain-English read of the
flags — then confirm it against your capture and `man tcpdump`.

## Connects forward
Reading the wire underpins Offensive recon/scanning, Defensive network monitoring
(Zeek/Suricata), and Forensic network reconstruction.

## Marketable proof
> "I can take a packet capture cold and walk the DNS lookup and the TCP handshake — and
> script the triage."

## Stretch
- Capture an HTTPS request (`curl https://example.com`): you'll see the TLS ClientHello but
  not the payload. Explain why — and what a defender can still learn from the metadata.
