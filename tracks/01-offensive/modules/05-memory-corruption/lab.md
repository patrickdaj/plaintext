# Lab 05 — Overflow a Buffer and Take Control

## Setup

```bash
git clone https://github.com/plaintext-security/plaintext-labs.git
cd plaintext-labs/offensive/05-memory-corruption
make up
```

The container ships `gcc`, `gdb`, and `python3`. The vulnerable C program
(`src/vuln.c`) is compiled inside the container with mitigations disabled
so the mechanism is visible.

## Scenario

Meridian Financial's intranet auth stub (`meridian-login`) was compiled by a
junior dev without hardening flags. You've got the binary. Demonstrate stack
smashing: find the offset that controls the saved instruction pointer, then
redirect execution to a function that was never supposed to be reachable.

> **Authorization note:** Only exploit systems you own or have explicit written
> permission to test. This binary is intentionally vulnerable; run it inside
> the provided container only.

## Do

1. [ ] Run the demo to see the full pipeline:
   ```bash
   make demo
   ```
   Note the offset (80 bytes), the win() address, and the exit code check.

2. [ ] Read `src/vuln.c`. Identify the vulnerable line. Draw the stack frame:
   - Where is `buf[64]` relative to the saved return address?
   - What local variable is between `buf` and the saved RBP?

3. [ ] Trace `exploit.py` step by step:
   - How does `get_win_addr()` find the target address?
   - How does `find_offset()` confirm the right offset without gdb?
   - What does `struct.pack("<Q", win_addr)` produce, and why little-endian?

4. [ ] Observe the crash output (Step 4). The exit code is negative — why?
   What does `0x4141414141414141` in RIP tell you?

5. [ ] Shell into the container and use gdb to confirm the overwrite:
   ```bash
   make shell
   python3 exploit.py --build
   gdb -q /tmp/meridian-login
   (gdb) run <<< $(python3 -c "import sys; sys.stdout.buffer.write(b'A'*200)")
   (gdb) info registers rip
   ```

6. [ ] In `src/vuln.c`, add `-fstack-protector` to the compile command in the
   comment, then compile manually and re-run the overflow payload. What changes?

## Success criteria — you're done when

- [ ] You can draw the stack frame for `vuln()` and explain why offset=80.
- [ ] You redirected execution to `win()` (exit code 42) with your own crafted payload.
- [ ] You can explain what mitigations (canary, ASLR, NX) each individually prevent — and why "NX alone" doesn't stop ret2win.
- [ ] You can state why memory-safe languages (Rust, Go) eliminate this class entirely.

## Deliverables

`overflow.md`: the vulnerable line, the stack diagram with offsets, the exploit
payload (hex), and a three-line argument for which mitigation matters most.
(Don't commit compiled binaries.)

## Automate & own it

**Required.** Write or extend `exploit.py` to:
- Accept a target binary path as an argument
- Automatically find the offset and any `win()`-style function
- Output a crafted payload to stdout (for piping)

AI drafts the script; you step through each function in gdb to verify the
offsets before committing. Commit `exploit.py` and `overflow.md`.

## AI acceleration

Ask a model to annotate the disassembly of `vuln()` (paste the `objdump -d`
output) and explain each instruction. Then verify against gdb — the model
accelerates reading assembly; the debugger is ground truth.

## Connects forward

This is the primitive under every "RCE via memory corruption" CVE. Track 04
(malware) references shellcode injection; Track 06 (Active Directory) covers
ROP chains used in privilege escalation from kernel exploits.

## Marketable proof

> "I can demonstrate a stack buffer overflow — from crash to controlled
> instruction pointer — and explain the mitigation chain (canary → ASLR → NX)
> and why each one alone is insufficient."

## Stretch

- Recompile with `-fstack-protector` and observe the canary inserted between
  the buffer and saved RBP. What error does GCC emit when you overflow?
- Recompile with `-pie` (ASLR-enabled) and try to run the same exploit. Why
  does it fail? What would you need to make it work again?
