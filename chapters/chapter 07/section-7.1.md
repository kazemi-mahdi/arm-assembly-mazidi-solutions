
---
chapter: 7
section: 7.1
file_role: "Solutions"
title: "Section 7.1 — ARM Pipeline Evolution (Mazidi)"
notes: "Classic ARM7 cores use a **3‑stage** pipeline; ARM9 moves to a **5‑stage** pipeline that separates memory and write‑back for higher throughput."
last_updated: 2025-08-31
---

# Chapter 7 · Section 7.1 — Exercises (Mazidi)

> Problems are paraphrased to respect copyright. Short, teachable answers below.

---

### 1) The **ARM7** uses a pipeline of ______ stages.  
**Answer:** **3 stages.**

---

### 2) Give the names of the pipeline stages in the **ARM7**.  
**Answer:** **Fetch → Decode → Execute.**

---

### 3) The **ARM9** uses a pipeline of ______ stages.  
**Answer:** **5 stages.**

---

### 4) Give the names of the pipeline stages in the **ARM9**.  
**Answer:** **Fetch → Decode → Execute → Memory → Write‑back.**

---

## Notes for learners
- ARM7’s 3‑stage design keeps things simple but limits clock speed.  
- ARM9 separates the **memory** access and **write‑back** phases, enabling better overlap and higher frequencies (with hazards handled by the core).
