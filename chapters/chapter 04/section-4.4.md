---
chapter: 4
section: "4.4"
file_role: Solutions
title: Chapter 4 · Section 4.4 — Exercises (Mazidi)
notes: See Mazidi, Ch. 4 section 4.4.
last_updated: 2025-09-01
---


# Chapter 4 · Section 4.4 — Exercises (Mazidi)

> Problems are paraphrased to respect copyright. Answers assume ARM (A32) where most instructions include a **condition field**.

---

### 31) Which bits of the ARM instruction are set aside for **condition execution**?
**Answer:** **bits [31:28]** — the 4‑bit **cond** field (e.g., `EQ/NE/CS/CC/.../AL`).

---

### 32) True or False. Only **ADD** and **MOV** have the conditional execution feature.
**Answer:** **False.** In ARM state, **nearly all instructions** (data processing, loads/stores, branches, etc.) have the **cond** field; the default is **AL** (always).

---

### 33) True or False. In ARM, the **conditional execution is default**.
**Answer:** **True.** Every instruction encodes a condition; when no suffix is written, it means **AL** (execute **always**).

---

### 34) Which flag is examined before the instruction **MOVEQ** executes?
**Answer:** The **Z (zero)** flag — `EQ` means **Z = 1**.

---

### 35) Difference between **ADDEQ** and **ADDNE**.
**Answer:** Both add, but **ADDEQ** executes only if **Z = 1** (equal), whereas **ADDNE** executes only if **Z = 0** (not equal).

---

### 36) Difference between **BAL** and **B**.
**Answer:** **No functional difference** in ARM state. `BAL` is just `B` with the explicit **AL** condition (branch **always**).

---

### 37) Difference between **SUBCC** and **SUBCS**.
**Answer:** The operation is the same (`SUB`), but the condition differs:  
- **CC** = **C = 0** (carry clear → **borrow occurred**, unsigned **<**).  
- **CS** = **C = 1** (carry set → **no borrow**, unsigned **≥**).

---

### 38) Difference between **ANDEQ** and **ANDNE**.
**Answer:** **ANDEQ** executes if **Z = 1**; **ANDNE** executes if **Z = 0**.

---

### 39) True or False. The decision to execute **SUBCC** is based on the **Z** flag.
**Answer:** **False.** `CC` is based on the **C (carry)** flag being **0**.

---

### 40) True or False. The decision to execute **ADDEQ** is based on the **Z** flag.
**Answer:** **True.** `EQ` tests **Z = 1**.

---

## Notes for learners
Common condition suffixes (test on CPSR **N,Z,C,V**):  
- `EQ` Z=1, `NE` Z=0  
- `CS/HS` C=1, `CC/LO` C=0  
- `MI` N=1, `PL` N=0  
- `VS` V=1, `VC` V=0  
- `HI` C=1 & Z=0, `LS` C=0 or Z=1  
- `GE` N==V, `LT` N!=V, `GT` Z=0 & N==V, `LE` Z=1 or N!=V  
- `AL` always
