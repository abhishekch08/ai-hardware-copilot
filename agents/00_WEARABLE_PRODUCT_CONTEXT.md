# Wearable Reference Product Context

This file is the shared physical-product reference for all agents in `agents/`. It does **not** replace the AI Hardware Engineer / Lab Copilot thesis. It gives the virtual company a concrete, difficult hardware program against which specialist behavior can be made operational rather than generic.

The reference program is a **compact, all-day, skin-contact wearable** in the temple/ear/head region. The exact commercial design may change. Agents must treat the architecture below as a working reference, not as immutable requirements.

---

## 1. Reference product class

Assume a device with the following characteristics unless a task states otherwise:

- very small body-worn electronics with severe PCB, enclosure and battery-volume constraints;
- direct or near-direct skin contact for many hours per day;
- BLE-class wireless connectivity to a phone and/or charger/accessory;
- ultra-low-power MCU/SoC, external or integrated nonvolatile memory and multiple switched power domains;
- optical sensing such as PPG/reflectance;
- IMU-based motion/activity/contact context;
- skin and/or ambient temperature sensing;
- optional biopotential, EDA, bioimpedance or other physiological channels depending on product generation;
- haptic, piezo or acoustic feedback where useful;
- a very small rechargeable Li-ion/Li-poly cell, with a separate charging accessory/dock possible;
- dense rigid, rigid-flex, flex or SiP/advanced-package implementation depending on maturity;
- metallic or partially metallic exterior surfaces that can materially affect RF, thermals, grounding and user perception;
- mobile applications, firmware, cloud/backend and data algorithms forming one end-to-end product;
- consumer/wellness positioning by default unless a specific program explicitly enters a regulated medical-device pathway.

This class of product creates coupled problems. An apparently local change can affect several domains simultaneously:

```text
smaller enclosure
  -> smaller battery
  -> lower energy budget
  -> altered radio duty cycle / sensor duty cycle
  -> changed signal quality
  -> changed algorithm performance
  -> changed user value

metal shell change
  -> antenna detuning / efficiency
  -> thermal spreading
  -> sensor thermal bias
  -> grounding / EMC behavior
  -> cosmetic and manufacturing consequences

skin-contact geometry change
  -> contact pressure
  -> optical coupling / motion artifact
  -> temperature bias
  -> comfort / retention
  -> demographic fit / repeatability
```

No specialist may optimize only its local metric when the system consequence is material.

---

## 2. Engineering objectives

Agents should reason against explicit budgets rather than adjectives. Typical product-level budgets include:

- **energy/runtime:** average current by state, pulse current, usable cell energy, charge time, storage drain and ship-mode leakage;
- **size:** PCB area, package height, enclosure wall/feature constraints, antenna volume, optical stack height, adhesive/bond-line volume and assembly access;
- **mass and comfort:** device mass, contact pressure, local pressure peaks, retention stability and all-day discomfort risk;
- **signal quality:** physiological signal amplitude, SNR, artifact burden, sensor saturation margin, calibration error and data yield;
- **thermal:** component junction temperature, skin-contact temperature, sensor self-heating and cross-heating between electronics and physiological temperature channels;
- **RF:** conducted output, matching, total efficiency, bandwidth, body detuning, coexistence, packet reliability and regulatory margin;
- **latency/storage:** sampling, buffering, synchronization, packetization, local storage and mobile/cloud latency;
- **reliability:** sweat, skin oils, cosmetics, humidity, thermal cycling, drop, torsion, charging cycles, adhesive aging, connector wear and cleaning exposure;
- **manufacturing:** yield, inspectability, calibration time, assembly takt, rework strategy, process capability and supplier variation;
- **cost:** BOM, advanced packaging, tooling, test time, yield loss, accessory cost, warranty/returns and cloud/service cost.

Every material recommendation should identify which budgets improve, which degrade and what evidence resolves the trade-off.

---

## 3. Reference sensing stack

### Optical / PPG

Agents should consider:
- emitter wavelength and current;
- photodiode geometry and optical path;
- skin-tone and tissue variability;
- ambient-light rejection;
- motion artifact;
- saturation/headroom;
- mechanical pressure/contact;
- optical barrier and leakage paths;
- LED self-heating;
- synchronization with IMU and algorithms;
- duty cycling and average power.

### IMU

Consider:
- physical axis orientation in the final body coordinate frame;
- ODR, bandwidth and anti-aliasing;
- full-scale range and clipping;
- vibration/mechanical coupling;
- synchronization to physiological channels;
- motion/context classification;
- calibration, bias and temperature drift;
- interrupt/FIFO strategy for power reduction.

### Temperature

Treat temperature as a coupled thermal-estimation problem, not merely a sensor-accuracy problem. Consider:
- true skin temperature versus measured package/PCB temperature;
- ambient coupling;
- electronics self-heating;
- thermal contact resistance;
- sensor placement and copper spreading;
- transient settling/time constant;
- calibration across ambient and activity conditions;
- estimation/model uncertainty and ground-truth instrumentation.

### Optional bioelectrical channels

For EEG/biopotential, EDA or bioimpedance variants, consider:
- electrode material and polarization;
- electrode-skin impedance and motion;
- bias/common-mode architecture;
- input protection and leakage;
- interference from digital, RF, haptics and charging;
- channel gain/dynamic range;
- safety and user-contact current limits;
- calibration and scientifically valid interpretation.

---

## 4. Power and battery doctrine

For a small wearable, energy is a first-class system architecture variable.

Every feature should have:

```text
state -> current -> duty cycle -> average current -> energy/day -> user value
```

Battery analysis must include more than nominal capacity:
- usable capacity over voltage and temperature;
- protection cutoffs;
- converter dropout/efficiency;
- pulse-load voltage sag and cell impedance;
- aging and cycle life;
- shipping/storage leakage;
- charger and accessory losses;
- brownout/recovery behavior;
- worst-case radio/sensor/haptic concurrency.

A feature that consumes little average energy can still cause a reset if its peak load collapses the cell/rail.

---

## 5. Mechanical, skin and industrial-design doctrine

The human body is a variable, compliant, warm, moist boundary condition. CAD nominal fit is insufficient.

Agents must account for:
- anthropometric variation;
- hair and skin variation;
- sweat, oils and cosmetics;
- local curvature and motion;
- pressure distribution and retention;
- long-duration comfort;
- don/doff behavior;
- cleaning;
- charging/storage workflow;
- skin-compatible materials and finishes;
- optical/RF/thermal consequences of housing materials;
- assembly and sealing after adhesives/resins cure and tolerances stack.

---

## 6. Software and data architecture doctrine

The product is a distributed system:

```text
sensors
 -> firmware acquisition
 -> timestamping / buffering
 -> on-device processing
 -> BLE / accessory transport
 -> mobile application
 -> backend / storage
 -> algorithm / model
 -> user-facing metric or action
```

Any metric defect may originate anywhere in that chain. Agents must preserve:
- sensor raw-data access where feasible;
- exact firmware and algorithm versions;
- timestamps and synchronization metadata;
- calibration coefficients;
- data-quality flags;
- device/configuration identity;
- algorithm confidence/validity conditions;
- reproducible processing.

Do not let a visually plausible app metric hide raw-signal or synchronization defects.

---

## 7. Product-development lifecycle

Agents should understand the distinction between learning builds and qualification builds.

### Concept / architecture
Prove sensing physics, ergonomics, battery feasibility, antenna feasibility and user value before over-optimizing packaging.

### EVT-like stage
Prove core electrical/mechanical architecture, bring-up, sensor SNR, power states, RF, thermal behavior and debug observability. Expect rework and instrumentation.

### DVT-like stage
Prove requirements across corners, environmental/reliability tests, user-fit variation, sealing, EMC/RF, battery behavior, calibration robustness and design-for-manufacture/test.

### PVT-like stage
Prove production process capability, yield, end-of-line test, calibration, traceability, station correlation, work instructions and supply continuity.

### Field / sustaining
Use returns, telemetry, manufacturing data and support evidence to update FMEA, design rules and future revisions.

No agent should use EVT evidence as if it were mass-production capability evidence.

---

## 8. Required reasoning standard for every specialist

For consequential work, every specialist should make the following explicit:

1. **Objective** — what is being optimized or decided?
2. **Known configuration** — exact revision/state relevant to the conclusion.
3. **Governing mechanism** — physics, protocol, process or business mechanism.
4. **Assumptions** — especially any unverified geometry, loads, material properties or user conditions.
5. **Calculations / evidence** — not just qualitative judgment.
6. **Competing explanations or options** — at least where ambiguity is material.
7. **Cross-domain effects** — what other agents/budgets are affected?
8. **Validation method** — how the recommendation will be falsified or confirmed.
9. **Decision status** — hypothesis, recommendation, approved design, verified result or production-proven result.
10. **Residual risk** — what remains unknown after the proposed work?

---

## 9. Human and regulatory boundary

By default this reference program is a **consumer wellness wearable**. Physiological measurements can still create substantial user-safety, privacy and claim risk.

Agents must not silently convert exploratory correlations into medical claims. Any transition toward diagnosis, treatment, clinical decision support or regulated medical use requires explicit regulatory, clinical/scientific, quality-system and risk-management work.

Data involving physiological signals should be handled as high-sensitivity user data even where local law does not label every field identically.

---

## 10. Definition of a useful agent

A useful specialist agent is not one that can describe its discipline. It must be able to take project artifacts and produce executable engineering work.

For example, an antenna agent should be able to turn enclosure/PCB geometry into keepout and tuning requirements plus an OTA experiment. A battery agent should be able to turn measured current traces and cell data into a runtime/voltage-sag model. A thermal agent should be able to separate body temperature, ambient temperature and self-heating with a model and test plan. A manufacturing agent should be able to turn the assembly into a process window and CTQ list.

That level of specificity is the standard expected from every description in this folder.
