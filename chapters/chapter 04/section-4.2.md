---
chapter: 4
section: "4.2"
file_role: Solutions
title: Chapter 4 · Section 4.2 — Exercises (Mazidi)
notes: See Mazidi, Ch. 4 section 4.2.
last_updated: 2025-09-01
---


# Chapter 4 · Section 4.2 — Exercises (Mazidi)

> Problems are paraphrased to respect copyright. Short teaching notes follow each answer.

---

### 17) **BL** is a(n) ___‑byte instruction.  
**Answer:** **4 bytes.**  
**Why:** In **ARM state** the encoding is a single 32‑bit word. *(In Thumb, `BL` is encoded as two 16‑bit halfwords—still 32 bits total.)*

---

### 18) In ARM, which register is the **link register**?  
**Answer:** **R14 (LR).**  
**Why:** `BL` writes the **return address** into **LR**.

---

### 19) True or False. The **BL** target address can be anywhere in the 4‑GB byte address space.  
**Answer:** **False.**  
**Why:** `BL` is **PC‑relative** with a **signed 24‑bit immediate (<<2)**; the branch range is about **±32 MB** from the call site.

---

### 20) Describe how we can **return** from a subroutine in ARM.  
**Answer:** Restore **PC** from **LR**, typically with **`BX LR`** (preferred, preserves state) or **`MOV PC,LR`**. If LR was saved on the stack, use **`POP {{PC}}`** (or load LR then `BX LR`).

---

### 21) In ARM, **which address is saved** when the **BL** instruction executes?  
**Answer:** The **return address**—i.e., the **address of the instruction following `BL`**—is saved in **LR (R14)**. *(Architecturally, it is the next sequential instruction address.)*

---

## Notes for learners
- `BLX` calls via a register or immediate and can **switch state** (ARM↔Thumb).  
- Typical subroutine prologue/epilogue on MCUs: `PUSH {{LR}}` … `POP {{PC}}` (or `BX LR`) if the routine calls other functions.
