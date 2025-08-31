---
chapter: 1
section: 1.1
file_role: "Solutions"
toolchain: ["Keil armasm", "GNU as (arm-none-eabi-as)"]
target_cpu: ["ARMv7-M (Thumb-2)", "ARMv6-M (M0/M0+)"]
last_updated: 2025-08-31
---

# Chapter {chapter} · Section {section} — Exercises (Mazidi)

> **How to use**  
> - Paraphrase each problem (do not copy it).  
> - Cite the relevant page: “See Mazidi, p. NN”.  
> - Keep solutions semi step-by-step: brief yet explanatory.  
> - If code is required, include *complete, runnable* snippets.

---

## Exercise X.Y-1 — *Short paraphrase of the problem*  
**Reference:** See *Mazidi*, p. {page}  
**Concepts:** (e.g., addressing modes, flags, condition codes)

### Approach
- Bullet points: plan the registers/memory, expected flags, corner cases.

### Solution
```armasm
        AREA    |.text|, CODE, READONLY
        EXPORT  _start
        THUMB                   ; or ARM if targeting ARM state
_start:
        ; 1) Initialize inputs
        ; 2) Perform operation
        ; 3) Observe flags
        ; 4) Store/print result

        B       .               ; stop (placeholder for emulator)
        END
```

### Explanation (semi step-by-step)
1. **Setup:** what goes where and why.  
2. **Reasoning:** key lines, flags affected (N,Z,C,V).  
3. **Check:** expected register/memory state.

### Quick verification
- **Keil/µVision:** assemble & single-step.  
- **GNU toolchain:**  
  ```
  arm-none-eabi-as -mcpu=cortex-m3 -mthumb -o ex1.o ex1.s
  arm-none-eabi-objdump -d ex1.o
  ```

---

## Common pitfalls for Section {section}
- Misreading carry vs. borrow on SUB/SBC.  
- Confusing LSR vs. ASR.  
- Forgetting IT blocks in Thumb when using conditional execution.
