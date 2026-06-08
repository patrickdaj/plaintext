# Module 05 — Memory Corruption Primer

**Offensive Security** — *why a program crashes is often why it gets exploited.*

## Why this matters
Memory-corruption bugs — buffer overflows and their relatives — are the root of a huge share
of the most severe CVEs, and out-of-bounds writes sit at the very top of the CWE "most
dangerous weaknesses" list. You don't need to become an exploit developer, but you do need to
understand *why* writing past a buffer hands an attacker control, so a vulnerability class
like "stack overflow" stops being a magic phrase.

## Objective
Explain how a stack-based buffer overflow hijacks execution, and demonstrate one against a
simple vulnerable program in your lab.

## Learn (~4 hrs)

**Concept, then hands-on**
- [Intro to Binary Exploitation — Buffer Overflows #0: Intro / Basics / Setup (video)](https://www.youtube.com/watch?v=wa3sMSdLyHw) — a beginner-friendly start to how stack overflows work.
- [pwn.college (Arizona State, free)](https://pwn.college/) — work the **Memory Errors / Program Security** modules; the best free hands-on path into binary exploitation.

**Why it matters at scale**
- [MITRE CWE-787 — Out-of-bounds Write](https://cwe.mitre.org/data/definitions/787.html) — consistently the #1 most dangerous software weakness; the class you're learning.

## Key concepts
- The stack, the saved return address, and control flow
- What "overflow the buffer" actually overwrites
- Why this hands the attacker the instruction pointer
- Modern mitigations (ASLR, stack canaries, NX) — at a high level
- Memory-corruption classes (overflow, use-after-free, out-of-bounds write)

## AI acceleration
A model is a patient tutor for the concepts and the assembly — ask it to annotate a
disassembly or explain a stack canary. But generated exploit code for memory bugs is fiddly
and version-specific; expect to debug it yourself, which is exactly where the understanding
forms.
