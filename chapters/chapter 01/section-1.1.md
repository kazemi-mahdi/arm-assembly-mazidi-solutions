---
chapter: 1
section: 1.1
file_role: "Solutions"
title: "Section 1.1 — Introduction to Microcontrollers (Mazidi)"
notes: "Page hints refer to the book PDF: Chapter 1, §1.1 (~pp. 15–17 of the PDF)."
---

# Chapter 1 · Section 1.1 — Exercises (Mazidi)

> Problems are paraphrased to respect copyright. See *Mazidi*, **Chapter 1 §1.1** (“Introduction to Microcontrollers”), PDF ~pp. **15–17**.

---

### 1) True or False. A general-purpose microprocessor has on-chip ROM.  
**Answer:** **False.**  
**Why:** General-purpose microprocessors (e.g., x86) provide only the CPU and **require external ROM/RAM and I/O**. *(See §1.1, PDF p. ~15.)*

---

### 2) True or False. Generally, a microcontroller has on-chip ROM.  
**Answer:** **True.**  
**Why:** A microcontroller integrates **CPU + program ROM/Flash + RAM + I/O** on a **single chip**. *(§1.1, p. ~15–16.)*

---

### 3) True or False. A microcontroller has on-chip I/O ports.  
**Answer:** **True.**  
**Why:** On-chip **GPIO and peripheral interfaces** (timers/serial, etc.) are part of the MCU integration. *(§1.1, p. ~16.)*

---

### 4) True or False. A microcontroller has a fixed amount of RAM on the chip.  
**Answer:** **True.**  
**Why:** The MCU’s **on-chip RAM size is fixed** for a given device family/part number. *(§1.1, p. ~15–16.)*

---

### 5) What components are usually put together with the microcontroller onto a single chip?  
**Answer:** **CPU, program ROM/Flash, data RAM, I/O ports**, and typically **timers/counters** and **serial peripherals** (UART/SPI/I²C); many devices also integrate **ADC/PWM/interrupt controller**. *(§1.1, p. ~16.)*

---

### 6) Intel’s Pentium chips used in Windows PCs need external ______ and ______ chips to store data and code.  
**Answer:** **RAM and ROM (BIOS/Flash).**  
**Why:** The Pentium is a **microprocessor**—it relies on **external memory** for both data and program storage. *(§1.1, p. ~15.)*

---

### 7) List three embedded products attached to a PC.  
**Example answers:** **Keyboard, mouse, printer**.  
(Other valid examples: scanner, webcam, external modem, game controller.) *(General §1.1 examples.)*

---

### 8) Why would someone want to use an x86 as an embedded processor?  
**Answer (concise):** To leverage **PC compatibility and ecosystem**—abundant **development tools**, existing **software/OS support**, and **familiarity/performance** for certain embedded applications. *(§1.1 context.)*

---

### 9) Give the name and the manufacturer of some widely used 8-bit microcontrollers.  
**Answer (any three):**  
- **8051 family** — originally **Intel**; produced by many vendors (e.g., **NXP**, **Silicon Labs**, **Atmel/Microchip**).  
- **PIC** — **Microchip Technology**.  
- **AVR** — originally **Atmel** (now **Microchip**).  
(Also acceptable: **Zilog Z8**, **Motorola/Freescale 68HC05/08**.) *(Historical overview in §1.1.)*

---

### 10) In Question 9, which one has the most manufacture sources?  
**Answer:** **8051 family.**  
**Why:** It has been **second-sourced by many manufacturers** for decades. *(§1.1.)*

---

### 11) In a battery-based embedded product, what is the most important factor in choosing a microcontroller?  
**Answer:** **Power consumption (low-power operation).**  
**Why:** Directly impacts **battery life** (sleep/active current, clocking options). *(§1.1 design considerations.)*

---

### 12) In an embedded controller with on-chip ROM, why does the size of the ROM matter?  
**Answer:** It **limits the maximum program size** (firmware features, tables, libraries) and **affects cost/part selection**. *(§1.1.)*

---

### 13) In choosing a microcontroller, how important is it to have multiple sources for that chip?  
**Answer:** **Important.**  
**Why:** Multiple sources reduce **supply-risk**, improve **price/lead-time**, and ensure **long-term availability** and drop-in replacements (as with many **8051** parts). *(§1.1.)*

---

### 14) What does the term “third-party support” mean?  
**Answer:** Availability of **tools and resources from companies other than the MCU vendor**—e.g., **compilers, assemblers, debuggers, IDEs, RTOS, programmers, evaluation boards, libraries**. Strong third-party support shortens development time. *(§1.1.)*

---
