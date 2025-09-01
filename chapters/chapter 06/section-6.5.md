---
chapter: 6
section: "6.5"
file_role: Solutions
title: Chapter 6 · Section 6.5 — Exercises (Mazidi)
notes: In ARM state, the PC seen by an instruction equals **address_of_this_instruction + 8** (prefetch). In Thumb state it’s +4. All answers below assume **ARM (A32)** unless noted.
last_updated: 2025-09-01
---


# Chapter 6 · Section 6.5 — Exercises (Mazidi)

> Problems are paraphrased to respect copyright. Short derivations shown for each.

---

### 53) If `LDR R2,[PC,#8]` is located at address **0x300**, what memory address is accessed?

**ARM state rule:** `PC_effective = current_address + 8`.  
Here: `PC_effective = 0x300 + 0x8 = 0x308`.  
`EA = PC_effective + 0x8 = 0x308 + 0x8 = **0x310**`.

**Answer:** **0x00000310**.

---

### 54) Using **PC‑relative** addressing, write an `LDR` that accesses a location **0x20 bytes ahead** of itself.

We want `EA = current_address + 0x20 = (current_address + 0x8) + imm`.  
Therefore `imm = 0x20 − 0x8 = 0x18`.

```armasm
LDR     R2, [PC, #0x18]    ; accesses (this instruction address + 0x20)
```
*(In Thumb state, use `#0x1C` because PC = addr + 4.)*

---

## Notes for learners
- `ADR Rd, label` emits a PC‑relative add; `LDR Rd,=imm` is often assembled into a **literal load** via a PC‑relative address.
