---
chapter: 6
section: "6.2"
file_role: Solutions
title: Chapter 6 · Section 6.2 — Exercises (Mazidi)
notes: "ARM uses R13 as the SP. Classic ARM stacks are **full‑descending** (push: pre‑decrement SP, store; pop: load, post‑increment). `BL` writes the return address to **LR (R14)** — it does **not** touch the stack unless your code saves LR."
last_updated: 2025-09-01
---


# Chapter 6 · Section 6.2 — Exercises (Mazidi)

> Problems are paraphrased to respect copyright. Short, teachable answers below.

---

### 15) True or false. In ARM the **R13** is designated as stack pointer.
**Answer:** **True.** R13 is the architectural **SP** (banked per mode on classic ARM).

---

### 16) When **BL** is executed, how many **stack locations** are used?
**Answer:** **Zero.** `BL` stores the **return address** in **LR (R14)**; the stack is used **only if** your code saves LR (e.g., `PUSH {LR}`).

---

### 17) When **B** is executed, how many **stack locations** are used?
**Answer:** **Zero.** `B` is a plain branch and does **not** touch the stack.

---

### 18) In ARM, stack pointer is ______ register.
**Answer:** **R13 (SP)**.

---

### 19) Describe how the **return** operation is performed in ARM.
**Answer:** **Restore PC from LR.** Common sequences:
```armasm
BX   LR          ; preferred (keeps ARM/Thumb state)
; or
MOV  PC, LR      ; simple return
; if LR was saved on stack:
POP  {PC}         ; load PC from stack (also returns)
```
Prologue/epilogue pattern for subroutines that call others:
```armasm
PUSH {LR}      ; save caller’s return
...              ; body, may BL further routines
POP  {PC}      ; restore and return
```

---

### 20) Give the **size of the stack** in ARM.
**Answer:** **Not fixed by the ISA.** Stack size is configured by your **linker/RTOS** and limited by **RAM**. Each pushed register occupies **4 bytes** (32‑bit words); the stack **grows downward** on classic ARM (full‑descending).

---

### 21) In ARM, **which address is saved** when `BL` is executed?
**Answer:** The **address of the instruction following `BL`** (the **return address**) is saved into **LR (R14)**.

---

## Notes for learners
- Many exception/privileged modes have **banked SP/LR**, so **R13/R14** can differ per mode (e.g., IRQ vs Thread).  
- On Cortex‑M, `PUSH/POP` mnemonics expand to `STMDB/ LDMIA` with SP and handle multiple registers in one go.
