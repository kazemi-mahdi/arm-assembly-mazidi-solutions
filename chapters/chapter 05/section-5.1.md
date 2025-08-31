
---
chapter: 5
section: 5.1
file_role: "Solutions"
title: "Section 5.1 — Signed Numbers Concept (Mazidi)"
notes: "Two’s‑complement on 32‑bit ARM. Positive N → 0‑extended; negative −N → (invert N) + 1."
last_updated: 2025-08-31
---

# Chapter 5 · Section 5.1 — Exercises (Mazidi)

> Problems are paraphrased to respect copyright. Answers show the 32‑bit **two’s‑complement** representation (hex).

---

## How to convert (quick refresher)
- **Positive** values: write the hex value and **zero‑extend to 8 hex digits** (32 bits).  
- **Negative −N**: write `N` in hex (32‑bit), then **invert** (bitwise NOT) and **add 1**.

---

### 1) 32‑bit representations

| item | value | 32‑bit two’s‑complement |
|---|---:|---|
| (a) | −23 | **0xFFFFFFE9** |
| (b) | +12 | **0x0000000C** |
| (c) | −0x28 | **0xFFFFFFD8** |
| (d) | +0x6F | **0x0000006F** |
| (e) | −128 | **0xFFFFFF80** |
| (f) | +127 | **0x0000007F** |
| (g) | +365 | **0x0000016D** |
| (h) | −32,767 | **0xFFFF8001** |

**Checks (sketch):**  
- (a) `23 = 0x00000017`; `~17 = 0xFFFFFFE8`; `+1 → 0xFFFFFFE9`.  
- (h) `32767 = 0x00007FFF`; `~ = 0xFFFF8000`; `+1 → 0xFFFF8001`.

---

### 2) 32‑bit representations

| item | value | 32‑bit two’s‑complement |
|---|---:|---|
| (a) | −230 | **0xFFFFFF1A** |
| (b) | +1200 | **0x000004B0** |
| (c) | −0x28F | **0xFFFFFD71** |
| (d) | +0x6FF | **0x000006FF** |

**Checks (sketch):**  
- (a) `230 = 0x000000E6`; `~ = 0xFFFFFF19`; `+1 → 0xFFFFFF1A`.  
- (c) `0x28F`; `~ = 0xFFFFFD70`; `+1 → 0xFFFFFD71`.

---

## Notes for learners
- The **sign bit** is bit31 (1 = negative).  
- Adding a positive number to its two’s‑complement negative gives **0** modulo `2^32`.  
- To verify: in most programmer’s calculators, set **word size = 32**, **two’s complement**, and toggle **DEC/HEX**.
