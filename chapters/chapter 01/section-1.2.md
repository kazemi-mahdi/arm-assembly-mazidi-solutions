---
chapter: 1
section: "1.2"
file_role: "Solutions"
title: "Section 1.2 — The ARM Family History (Mazidi)"
notes: "Page hints refer to the book’s Chapter 1, §1.2 (~pp. 17–20 of the PDF)."
last_updated: 2025-09-01
---

# Chapter 1 · Section 1.2 — Exercises (Mazidi)

> Problems are paraphrased to respect copyright. See *Mazidi*, **Chapter 1 §1.2** (“The ARM Family History”), PDF ~pp. **17–20**.

---

## Quick scan (True/False)
15 **—** n/a • 16 **False** • 17 **True** (with context) • 18 **True** • 19 **False** • 20 **True** •  
21 **False** • 22 **False** • 23 **True** • 24 **False** • 25 **False** • 26 **False**

---

### 15) What does ARM stand for?  
**Answer:** Originally **Acorn RISC Machine**; later **Advanced RISC Machines**. Today the company is **Arm Ltd.**  
**Why:** The project began at Acorn Computers and evolved into a standalone IP company. *(§1.2)*

---

### 16) True or False. In ARM, architectures have the same names as families.  
**Answer:** **False.**  
**Why:** **Architecture versions** are named **ARMv4/v5/v6/v7/v8**, while **product families** are **ARM7/ARM9**, **Cortex-A/R/M**, etc. Names are related but **not the same**. *(§1.2)*

---

### 17) True or False. In 1990s, ARM was widely used in the microprocessor world.  
**Answer:** **True** (in embedded/mobile).  
**Why:** ARM became the **dominant 32-bit RISC** in handhelds/embedded devices (PDAs, phones), even though desktop PCs remained x86. *(§1.2)*

---

### 18) True or False. ARM is widely used in Apple products, like iPhone and iPod.  
**Answer:** **True.**  
**Why:** Apple’s mobile devices use ARM-based SoCs. *(§1.2)*

---

### 19) True or False. Currently the Microsoft Windows does not support ARM products.  
**Answer:** **False.**  
**Why:** Microsoft has supported ARM in **Windows CE/Embedded, Windows Phone, and modern Windows on ARM**. *(§1.2 context)*

---

### 20) True or False. All ARM chips have standard instructions.  
**Answer:** **True** (core ISA is standardized per architecture version).  
**Why:** The **instruction set architecture (ARM/Thumb/Thumb-2, plus optional extensions like VFP/NEON)** is defined by Arm; implementations conform to the relevant spec. *(§1.2)*

---

### 21) True or False. All ARM chips have standard peripherals.  
**Answer:** **False.**  
**Why:** **Peripherals are vendor-specific** (UART, timers, GPIO mapping, ADC, etc.), so registers and drivers differ across manufacturers/families. *(§1.2)*

---

### 22) True or False. The ARM corporation also manufactures the ARM chip.  
**Answer:** **False.**  
**Why:** Arm is an **IP licensor**; **licensees** (e.g., ST, NXP, TI, Samsung, Microchip) manufacture the chips. *(§1.2)*

---

### 23) True or False. The ARM IP must be licensed from ARM corp.  
**Answer:** **True.**  
**Why:** Companies **license CPU cores/architectures** (soft/hard IP) from Arm to build their SoCs/MCUs. *(§1.2)*

---

### 24) True or False. A serial-communication program written for a TI ARM chip should run without any modification on a Freescale ARM chip.  
**Answer:** **False.**  
**Why:** While the **core ISA** is compatible, **peripheral registers/clock trees/interrupts** are different; **UART drivers** and init code are **not portable** without adaptation. *(§1.2)*

---

### 25) True or False. An Assembly program written for one family of ARM Cortex chip can execute on any other Cortex ARM chip.  
**Answer:** **False** (not universally).  
**Why:** Portability depends on **ISA mode** and **architecture level** (e.g., **Cortex-M** is **Thumb-2-only**, while **Cortex-A** may use **ARM/AArch32/AArch64**). Also, **system control** and memory maps differ. Pure, ISA-only code might port, but **in general modifications are required**. *(§1.2)*

---

### 26) True or False. At the present time, ARM has just one manufacturer.  
**Answer:** **False.**  
**Why:** There are **many** Arm licensees (ST, NXP, TI, Microchip/Atmel, Renesas, Samsung, etc.). *(§1.2)*

---

### 27) What is the difference between the ARM products of different manufacturers?  
**Answer (concise):**  
- **Same core architecture**, but **different peripherals** (timers, UART, I²C/SPI, ADC, PWM), **memory sizes**, **clock trees**, **packages**, **power modes**, and **toolchain support**.  
- Result: **software drivers, BSPs, and startup code** are **vendor/family specific** even when the CPU core is the same. *(§1.2)*

---

### 28) Name some 32-bit microcontrollers.  
**Examples (any correct subset):**  
- **STM32** (STMicroelectronics, Cortex-M)  
- **NXP LPC / i.MX RT** (Cortex-M)  
- **TI Tiva-C / MSP432** (Cortex-M)  
- **Microchip SAM** (ex-Atmel, Cortex-M)  
- **Renesas RA** (Cortex-M)  
- **PIC32** (Microchip, MIPS-based — still 32-bit MCU)  
*(§1.2 examples/history)*

---

### 29) What is Intel’s challenge in decreasing the power consumption of the x86?  
**Answer:** Maintaining **backward compatibility** with the complex legacy **x86 ISA** (variable-length decode and large micro-architectural support) imposes **power/complexity overheads**. Reducing power while keeping performance and compatibility is the key challenge compared to lean RISC designs like ARM. *(§1.2 discussion)*

---
