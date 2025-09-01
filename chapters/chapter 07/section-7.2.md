---
chapter: 7
section: "7.2"
file_role: Solutions
title: Chapter 7 · Section 7.2 — Exercises (Mazidi)
notes: Superpipeline = more (finer‑grained) pipeline stages. Superscalar = multiple execution units/issue slots. Most modern cores fetch in order, may execute out of order, and retire in order.
last_updated: 2025-09-01
---


# Chapter 7 · Section 7.2 — Exercises (Mazidi)

> Problems are paraphrased to respect copyright. Short, teachable answers follow.

---

### 5) The number of pipeline stages in a **superpipeline** system is ______ (less, more) than in a superscalar system.  
**Answer:** **more.** Superpipelining splits work into **more, shorter stages** to raise the clock; superscalar focuses on **parallel units** rather than stage count.

---

### 6) Which has **one or more execution units**, superpipeline or superscalar?  
**Answer:** **Superscalar.** It issues to **multiple functional units** per cycle (ALUs, load/store, etc.).

---

### 7) Which part of on‑chip cache in ARM is **write‑protected**, data or code?  
**Answer:** **Code (instruction) cache.** The CPU doesn’t write instructions directly; fills/evictions happen via the memory system, while data cache is writable by stores.

---

### 8) What is **instruction pairing**, and when can it happen?  
**Answer:** Pairing means **issuing/executing two instructions in the same cycle**. It occurs on **superscalar** cores when the two instructions are **independent**, target **different execution units/ports**, and satisfy alignment/resource rules (no hazards).

---

### 9) What is **data dependency**, and how is it avoided?  
**Answer:** A situation where one instruction **needs the result** of another (RAW) or conflicts on destinations (WAW) or sources (WAR). Avoided by **reordering**, **register renaming**, **forwarding/bypassing**, or inserting **stalls** when necessary.

---

### 10) True/False — Instructions are **fetched** according to the order in which they were written.  
**Answer:** **True.** Fetch is in **program order** (subject to branch prediction).

---

### 11) True/False — Instructions are **executed** according to the order in which they were written.  
**Answer:** **False.** Modern CPUs may **execute out of order** to hide latencies.

---

### 12) True/False — Instructions are **retired** according to the order in which they were written.  
**Answer:** **True.** **In‑order retirement (commit)** preserves precise exceptions and architectural state.

---

### 13) The visible registers **R0, R1, …** are updated by which unit of the CPU?  
**Answer:** The **write‑back/retire stage** (register file write‑back).

---

### 14) True/False — Among the instructions, **STR** (store) operations are **never executed out of order**.  
**Answer:** **False.** Stores may be **issued/out‑of‑order** and buffered; however, they are typically **made visible (committed) in order** to maintain memory consistency.

---

## Notes for learners
- Two orthogonal levers for speed: **deeper pipelines** (superpipeline) and **wider issue** (superscalar).  
- Out‑of‑order execution + in‑order retirement is the common combination in ARM performance cores.
