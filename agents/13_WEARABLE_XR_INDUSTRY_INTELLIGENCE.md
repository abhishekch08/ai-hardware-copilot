# Wearable and XR Industry Intelligence Handbook

**Knowledge snapshot:** 2026-09-11  
**Purpose:** Give every relevant agent deep, current, public-evidence-based knowledge of wearable and spatial-computing product practice without confusing those products with the company's primary AI Hardware Engineer / Lab Copilot mission.

This is a living intelligence specification, not a claim that an AI agent has worked inside any named company or knows proprietary designs. Product names, specifications, features, prices, subscriptions, claims, and platform policies change. Consequential work must refresh the relevant facts from primary sources and record retrieval date, region, generation, and confidence.

## 1. Why this knowledge matters to the Lab Copilot

Wearables compress nearly every hard product-development constraint into a small volume:

- microwatts and microamps matter while radio, optical, compute, audio, and haptics create large peaks;
- antenna, battery, metal, body, optical windows, sensors, and mechanics compete for the same space;
- the measurand passes through tissue/contact/mechanics before electronics and algorithms see it;
- firmware, synchronization, calibration, mobile OS behavior, cloud processing, and UI can invalidate otherwise good hardware;
- cosmetic finish, comfort, charging, data trust, service, and subscription design affect retention as much as sensor count;
- mass production must control tiny tolerances, adhesives, optics, flex, batteries, sealing, calibration, and RF variation.

These products supply realistic benchmark cases for design ingestion, mixed-signal reasoning, power debugging, sensor validation, RF/mechanical coupling, failure analysis, configuration control, and evidence-grounded reporting.

## 2. Intelligence evidence contract

Every company/product claim should be stored as:

```yaml
company:
product_family:
generation:
market_region:
as_of_date:
claim:
evidence_class: official_spec | developer_doc | regulatory | patent | paper | source_code | teardown | review | inference
source:
conditions_or_scope:
confidence:
engineering_interpretation:
unknowns:
relevance_to_lab_copilot:
```

### Evidence priority

1. official specifications, support documents, developer APIs, regulatory filings, standards, and released source code;
2. peer-reviewed validation using the identified device/generation;
3. patents for possible mechanisms only - never proof that a shipped product uses the mechanism;
4. high-quality measured teardown or bench characterization;
5. company marketing claims, clearly labeled as claims;
6. reviews, forums, and anecdotes for hypothesis generation only.

### Mandatory distinctions

- `advertised battery life` versus measured runtime under a stated workload;
- `sensor present` versus raw access, sampling behavior, data quality, and validated metric;
- `water-resistance rating` versus long-term sweat, cleaning, seal aging, and warranty behavior;
- `correlation` versus agreement or clinical/engineering accuracy;
- `feature available` versus region, device generation, OS, subscription, and regulatory dependence;
- `patented` versus implemented;
- `teardown observation` versus schematic-level certainty;
- `product strategy inference` versus verified internal rationale.

## 3. Required analysis layers for every benchmark

| Layer | Questions agents must answer |
|---|---|
| User and job | Who wears it, where, for how long, and what behavior/action follows from the output? |
| Form factor | Wrist, ring, ear, head, patch, garment, glasses, accessory; display/no display; body coupling and retention. |
| Sensing | Measurand, sensor modality, wavelengths/electrodes/axes, placement, contact, artifact, sampling, calibration, and ground truth. |
| Electronics | SoC/MCU, AFE, memory, PMIC, clocks, interfaces, protection, debug/test access, packaging, rigid/flex/SiP choices. |
| Energy | Cell form, usable energy, load states, peak delivery, charging architecture, accessory, runtime, aging, thermal limits. |
| RF and connectivity | BLE/Wi-Fi/cellular/GNSS/UWB/NFC/ANT+, antenna/body/enclosure interaction, coexistence, offline behavior. |
| Mechanics/CMF | Stack, material, seal, adhesives, flex, tolerances, comfort, finish, corrosion, cleaning, repair, recyclability. |
| Firmware | Acquisition, timing, FIFO/DMA, power states, OTA, fault recovery, logs, production modes, security. |
| Algorithms/data | Signal quality, fusion, personalization, confidence, data lineage, on-device/phone/cloud partition, model updates. |
| Experience/ecosystem | Onboarding, wear/charge habit, notifications, app interpretation, APIs, third-party ecosystem, accessibility. |
| Validation/claims | Requirements, population, motion/environment, reference method, failure rate, privacy, medical/wellness boundary. |
| Manufacturing/service | Suppliers, assembly CTQs, test/calibration, yield, genealogy, repair/replacement, warranty/returns. |
| Business | Hardware margin, subscription, attach/accessory, platform lock-in, distribution, upgrade cycle, support burden. |
| Lab Copilot relevance | Which design/debug workflow, evidence schema, tool integration, or benchmark case should be learned? |

## 4. Major company and ecosystem dossiers

These dossiers describe the **questions and demonstrated public product patterns** each specialist must know. They intentionally avoid unsupported internal component claims.

### 4.1 Apple

**Product families to track:** Apple Watch and Watch Ultra; AirPods/hearables; Apple Vision Pro and visionOS; HealthKit/WorkoutKit/Core Motion and relevant device/accessory frameworks; safety, accessibility, privacy, service, and environmental documentation.

**Engineering patterns to study**

- vertical integration across silicon, sensing, packaging, firmware, algorithms, operating system, phone/cloud ecosystem, retail/service, and claims;
- watch-scale mixed optical/electrical sensing, motion/context fusion, haptics/audio, wireless, display, and health/workout UX;
- compact SiP/packaging, flex interconnect, custom mechanical/CMF, charging, sealing, antenna coexistence, and production calibration;
- hearable constraints: acoustic seal/fit, microphones, speaker/ANC paths, head gestures, battery/case charging, per-ear synchronization, RF/body shadowing, and all-day comfort;
- spatial-computing integration: camera/IMU/eye/hand sensing, low-latency rendering, display optics, privacy, accessibility, and developer platform boundaries;
- feature rollout conditioned by hardware generation, OS, geography, validation, and regulatory authorization;
- strong user-facing abstraction: sophisticated sensing is presented as decisions/actions rather than raw engineering metrics.

**Lab Copilot lessons**

- treat hardware, calibration, OS, app, algorithms, privacy, and service as one configuration-controlled product;
- create a clear boundary between reliable sensor evidence and user-facing inference;
- design optional spatial interfaces through a stable software platform rather than hard-coupling the product to one device;
- make accessibility, privacy indicators, updates, and failure recovery product architecture concerns.

**Primary starting points:** [Apple Watch](https://www.apple.com/watch/), [AirPods](https://www.apple.com/airpods/), [Apple Vision Pro](https://www.apple.com/apple-vision-pro/), [Apple Developer](https://developer.apple.com/), [Apple Machine Learning Research](https://machinelearning.apple.com/).

### 4.2 Google and Fitbit

**Product/platform families to track:** Pixel Watch; Fitbit trackers and services; Wear OS; Health Connect; Android sensor, BLE, camera, and XR platform APIs; published wearable/health ML research.

**Engineering patterns to study**

- combination of Fitbit longitudinal health/fitness experience with Pixel/Android software, ML, mobile services, and developer ecosystem;
- wrist optical/motion/electrical/temperature-class sensing and context-aware metric generation;
- phone-watch-cloud partition, background execution, permission models, data interoperability, and cross-device identity;
- the difference between platform APIs, device-internal raw signals, and consumer-facing derived metrics;
- heterogeneous Android device behavior, lifecycle, connectivity, and power-management constraints;
- multimodal and self-supervised wearable modeling research, with strict separation between research capability and shipped feature.

**Lab Copilot lessons**

- design an extensible data and plugin boundary while preserving exact device/configuration provenance;
- support heterogeneous host platforms and intermittent connectivity;
- use multimodal/context models without hiding raw-quality flags or transport timing;
- separate public API availability from what a first-party device can measure internally.

**Primary starting points:** [Google Pixel Watch](https://store.google.com/category/watches), [Fitbit](https://www.fitbit.com/), [Wear OS developers](https://developer.android.com/training/wearables), [Health Connect](https://developer.android.com/health-and-fitness/guides/health-connect), [Google Research](https://research.google/).

### 4.3 Samsung

**Product/platform families to track:** Galaxy Watch; Galaxy Ring; Galaxy Buds; Samsung Health; Wear OS collaboration; Galaxy XR/spatial-computing devices and developer support.

**Engineering patterns to study**

- multi-form-factor health ecosystem spanning wrist, ring, ear, and phone, with cross-device data/UX opportunities;
- shared sensor and algorithm concepts expressed differently under ring versus watch energy, fit, display, GNSS, RF, and charging constraints;
- compact optical/electrical sensing modules, motion/temperature context, wireless charging, waterproofing, and consumer manufacturing scale;
- Android ecosystem integration, device/phone interoperability, regional feature availability, and health-data platform considerations;
- industrial scale, broad price segmentation, supply/manufacturing depth, and coexistence among many radios/features.

**Lab Copilot lessons**

- represent one user/system across multiple physical devices and configurations;
- build form-factor-aware requirements rather than copy a feature from watch to ring;
- include multi-device timing, data reconciliation, and charger/accessory states in debug models;
- design benchmark cases around assembly variation and high-volume test/calibration.

**Primary starting points:** [Samsung wearables](https://www.samsung.com/us/watches/), [Galaxy Ring](https://www.samsung.com/us/rings/galaxy-ring/), [Samsung Health](https://developer.samsung.com/health), [Samsung Developer](https://developer.samsung.com/).

### 4.4 Meta

**Product/platform families to track:** Ray-Ban Meta smart glasses; Quest headsets; Meta Horizon OS and developer stack; hand/eye/body tracking; audio/camera AI; published Reality Labs research.

**Engineering patterns to study**

- displayless AI glasses using camera, microphones, speakers, touch/voice, phone/cloud connectivity, capture indicators, charging case, and socially acceptable eyewear design;
- VR/MR headsets using inside-out tracking, multiple cameras, IMUs, controllers/hands, spatial audio, high-rate rendering, and video pass-through;
- privacy tension around always-available cameras/microphones, bystander awareness, capture indication, data retention, and AI services;
- head-worn battery, heat, weight distribution, optics, fit, prescription, latency, and connectivity trade-offs;
- large-scale developer platform and content/runtime compatibility versus specialized industrial workflows.

**Lab Copilot lessons**

- a useful hands-free interface may not require a display; voice/audio/camera can be tested first;
- social acceptability and privacy indicators are engineering requirements;
- generic scene AI is not equivalent to CAD-registered, uncertainty-bounded probe guidance;
- consumer headsets may validate interaction concepts while failing lab/PPE/security requirements.

**Primary starting points:** [Ray-Ban Meta](https://www.meta.com/smart-glasses/), [Meta Quest](https://www.meta.com/quest/), [Meta for Developers](https://developers.meta.com/), [Reality Labs Research](https://www.meta.com/emerging-tech/).

### 4.5 WHOOP

**Product family to track:** screenless recovery/strain/sleep wearable, sensor modules and bands/accessories, charging behavior, coaching/application, memberships, team/enterprise and research programs.

**Engineering patterns to study**

- screenless hardware shifts user value into continuous wear, low friction, app/coaching, longitudinal baselines, and subscription;
- recovery/strain/sleep products depend on consistent wear, optical contact, motion context, signal quality, and behaviorally meaningful interpretation;
- battery/charging choices are part of retention: charging without breaking a long data record is a product-system problem;
- strap material, fit, alternate body locations/accessories, sweat/water, cleaning, and exercise motion affect signals and durability;
- membership economics require recurring insight/service value rather than a one-time device feature list.

**Lab Copilot lessons**

- optimize for completed engineering outcomes and continuous workflow, not feature-display density;
- measure interruption cost, setup friction, and longitudinal evidence continuity;
- model accessories and charging as part of the device state/configuration;
- build sensor-debug benchmarks that use motion, fit, and context rather than clean stationary traces.

**Primary starting points:** [WHOOP](https://www.whoop.com/), [WHOOP support](https://support.whoop.com/), [WHOOP research](https://www.whoop.com/thelocker/tag/research-studies/).

### 4.6 Oura

**Product family to track:** Oura Ring, charger/sizing workflow, Oura app and membership, sleep/readiness/activity/stress/women's-health features, APIs/integrations, and published validation.

**Engineering patterns to study**

- finger location can provide strong optical/temperature signals but creates ring-size, rotation, contact, swelling, impact, scratch, and charger-alignment constraints;
- multi-day, displayless operation requires aggressive duty cycling, tiny battery/package integration, robust timekeeping/buffering, and app-centered experience;
- sizing kit and fit are part of sensing performance and returns economics, not merely retail packaging;
- metric trust depends on longitudinal personalization, data-quality handling, clear claims, and validation across populations/conditions;
- small metal-rich geometry makes antenna, charging, sealing, finish, comfort, and manufacturing tolerance tightly coupled.

**Lab Copilot lessons**

- ingest mechanical fit and user-contact state when diagnosing sensor quality;
- connect a field symptom to size, lot, finish, battery age, firmware, calibration, and algorithm version;
- benchmark tiny-product assembly, charging, RF, optical, and temperature interactions;
- represent absence/invalid data rather than fabricate a plausible metric.

**Primary starting points:** [Oura Ring](https://ouraring.com/), [Oura API](https://cloud.ouraring.com/docs/), [Oura Science](https://ouraring.com/science-and-research).

### 4.7 Garmin

**Product/platform families to track:** multisport/outdoor watches, fitness trackers, cycling computers/sensors, inReach and navigation products, chest straps, Connect IQ, Garmin Connect, FIT SDK, Garmin Health APIs/SDKs, and ANT wireless ecosystem.

**Engineering patterns to study**

- portfolio segmentation by sport, ruggedness, navigation, endurance, display, materials, size, and price rather than one universal wearable;
- long battery life through product-specific display/GNSS/sensor/connectivity policies and explicit activity modes;
- GNSS, altimetry, maps, sensors, physiological metrics, buttons/touch, outdoor readability, water/ruggedness, and offline use;
- structured activity data, external sensors, Connect IQ/FIT/ANT+ ecosystems, and backward compatibility;
- reliability for heat/cold/water/shock/long events and user trust in navigation/training data.

**Lab Copilot lessons**

- build device capability discovery and mode-aware specifications rather than assuming uniform hardware;
- support long-duration offline sessions and structured interoperable data;
- route debugging using mission profile: indoor lab, outdoor field, endurance, harsh environment, or safety communication;
- treat button/control redundancy and graceful degradation as valuable engineering UX.

**Primary starting points:** [Garmin wearables](https://www.garmin.com/en-US/c/wearables-smartwatches/), [Garmin Developers](https://developer.garmin.com/), [FIT SDK](https://developer.garmin.com/fit/), [Connect IQ](https://developer.garmin.com/connect-iq/).

## 5. Startup and adjacent-company watchlist

The purpose is not a static “top companies” list. SCI-07 and MKT-02 maintain a dated watchlist across mechanism and business-model categories.

| Category | Representative companies/products to track | Engineering questions |
|---|---|---|
| Smart rings | Ultrahuman, RingConn, Circular, Movano/Evie, and new entrants | Fit/sizing, optical/temperature/motion sensing, tiny batteries, metal antenna/charging, sealing, finish, subscription, women's health/medical boundary. |
| Performance/recovery | Polar, Suunto, COROS, Amazfit/Zepp, Biostrap, FORM, and sport-specific devices | Sensor validity under motion, GNSS, training models, recovery interpretation, endurance, accessory ecosystem, price segmentation. |
| Hearables/ear sensing | Bose, Sony, Jabra, Apple, Samsung, ear-EEG/physiology startups | Acoustic fit, microphones/ANC, in-ear optical/temperature/electrode sensing, binaural timing, body shadowing, case charging, hygiene. |
| Neurotechnology | Muse, OpenBCI, Emotiv, Xtrodes, Earable Neuroscience, NextSense, Neurable, Nomad, Atlas and emerging ear/head systems | Electrode/contact physics, motion/EMI, scientific validity, form factor, dry electrodes, AFE safety, privacy, model/claim boundaries. |
| Patches/continuous monitors | Dexcom, Abbott, BioIntelliSense, Empatica, VitalConnect, Epicore and biosensor startups | Adhesion/skin, disposable/reusable partition, electrochemistry/optics, clinical validation, data continuity, regulated quality, logistics. |
| Metabolic/longevity ecosystems | Ultrahuman, Levels, January AI and related sensor/service companies | Sensor-source dependency, algorithm interpretation, subscription/coach value, claims, integrations, retention and data governance. |
| AI glasses | Meta/Ray-Ban, Brilliant Labs, Even Realities, Solos, Halliday and new entrants | Displayless versus display, camera/audio, compute offload, privacy indicator, battery/case, prescription/social acceptability, developer access. |
| XR display glasses | XREAL, VITURE, Rokid, TCL/RayNeo and similar platforms | Display optics, 3DoF/6DoF, tethering, latency, FOV/eye box, device compatibility, thermal and enterprise APIs. |
| Industrial AR | RealWear, Vuzix, Magic Leap and enterprise headset/workflow vendors | PPE, voice/noise, ruggedness, remote assist, work instructions, device management, offline use, ROI and integration. |
| Research/novel sensors | flexible electronics, textile sensors, sweat/chemical, ultrasound, optical spectroscopy, radar, heat-flux and non-invasive biomarker startups | Measurand validity, maturity, calibration, drift, selectivity, power, packaging, manufacturability and claim risk. |

For each watchlist entry, capture what changed, evidence strength, maturity, integration burden, supply/scale evidence, why it matters, and action: `IGNORE`, `WATCH`, `BENCH EVALUATE`, `PARTNER`, or `INTEGRATE`.

## 6. Cross-company benchmark matrices

### 6.1 Form-factor comparison

| Form | Strengths | Dominant engineering liabilities | Lab Copilot relevance |
|---|---|---|---|
| Watch | volume, display, interaction, multi-sensor, GNSS/connectivity | wrist motion/contact, display power, thickness, charge habit, body detuning | rich mixed-signal/RF/power/UX benchmark; possible remote status surface |
| Screenless strap | continuous wear, low distraction, app-centered service | fit variability, no local UI, subscription dependence, charge continuity | model uninterrupted engineering sessions and low-attention interaction |
| Ring | sleep comfort, finger optical/temperature opportunity, discreet | tiny battery/antenna, size SKUs, rotation/swelling, finish/seal/charger | severe miniaturization and configuration/manufacturing benchmark |
| Earbud/hearable | audio/voice, stable ear location, case ecosystem | tiny energy, occlusion/fit, hygiene, RF shadowing, binaural sync | displayless voice/audio interface and close-range sensing benchmark |
| Smart glasses | first-person camera, hands-free audio/optional display | privacy, heat, battery, fit, prescription, camera/display alignment | optional interface; existing hardware first |
| MR/VR headset | rich display, tracking, compute, mature spatial APIs | weight, occlusion, PPE, fatigue, isolation, cost | rapid spatial UI/CAD-overlay prototyping, not default lab attire |
| Patch | stable localized contact, continuous sensing | skin adhesion, consumables, irritation, disposal, regulatory burden | test of human/medical data rigor and disposable/reusable architecture |

### 6.2 Product-strategy comparison

| Pattern | Examples | What to study |
|---|---|---|
| Integrated ecosystem | Apple, Google/Fitbit, Samsung | hardware/software/data/service configuration and cross-device workflow |
| Subscription-led screenless insight | WHOOP, Oura and adjacent startups | recurring value, continuous wear, longitudinal baselines, trust and retention |
| Sport/outdoor portfolio | Garmin, Polar, Suunto, COROS | mission-profile segmentation, endurance, ruggedness, offline operation, external sensors |
| Camera/audio AI glasses | Meta and startups | hands-free benefit without HUD, privacy, cloud/phone offload, social acceptability |
| Spatial-computing platform | Apple, Meta, Google/Samsung ecosystem, enterprise XR | tracking/display/runtime/HCI integration and developer/platform boundaries |

## 7. Minute engineering knowledge expected by discipline

### Systems and product agents

Track form-factor and ecosystem choices, feature-to-user-value chain, charge/wear habits, display/no-display interaction, sensor/algorithm/claim dependency, subscription and service model, product generations, region/OS limits, accessibility, privacy, and return/abandonment mechanisms.

### Electrical, power, RF, and PCB agents

Understand optical/electrode/IMU/temperature signal chains; LED and radio pulse loads; PMIC modes and leakage; tiny-cell impedance/aging; charger/case/dock/contact/inductive trade-offs; dense rigid/flex/SiP layouts; ground/antenna/body/metal coupling; acoustic/haptic drivers; ESD/user-contact protection; and production test access.

### Mechanical, ID, CMF, and human-factors agents

Understand body-site anatomy and variation; pressure/retention/fit; ring sizing and swelling; ear seal/hygiene; head/nose/temple loads; sweat/sebum/cosmetics/cleaners; metal/polymer/elastomer/coating/adhesive interactions; sealing/vents; sensor optical windows; battery crush protection; flex strain; cosmetic aging; charging and don/doff behavior.

### Firmware, mobile, cloud, and data agents

Understand sensor timing, FIFOs, duty cycles, power-state transitions, event correlation, raw/derived data, BLE/GATT and reconnection, pairing/ownership transfer, OTA/rollback, phone background limits, offline buffering, schema evolution, calibration lineage, fleet observability, invalid-data states, and cross-device synchronization.

### Science, algorithms, and validation agents

Understand measurand-to-signal causal chain, body-site external validity, motion/contact/ambient/perfusion confounding, signal quality, subject/device/session leakage, ground truth, agreement not just correlation, population/subgroup limitations, claims boundaries, longitudinal personalization, and failure-rate/data-yield metrics.

### Manufacturing, quality, regulatory, and service agents

Understand cell/flex/optics/custom mechanical sourcing; micro-assembly; dispense/cure/alignment; size/color SKUs; RF/optical/calibration EOL; traceability; cosmetic criteria; water/sweat/reliability sequence; batteries/transport; radio/product/medical requirements; repairability; warranty; returns and field feedback.

### XR agents

Understand display/no-display product patterns; camera/IMU/audio/eye/hand sensors; optics and eye box; 3DoF/6DoF; SLAM/calibration/drift; voice/gaze/gesture failure; motion-to-photon and camera-to-overlay latency; weight/heat/PPE/privacy; platform APIs; enterprise device management; and task-level benefit.

## 8. Benchmark cases to encode for agent evaluation

Wearable-derived cases should include at least:

- idle current increases after firmware or BOM revision;
- optical channel clips only under sunlight or poor contact;
- motion artifacts masquerade as physiology;
- temperature rises with radio/LED duty cycle and biases the inferred metric;
- BLE range collapses after metal/finish/battery/enclosure change;
- wrong IMU axis/body-frame mapping corrupts context;
- tiny cell resets system during concurrent radio/LED/haptic peaks;
- sensor fails to enter sleep because of bus/GPIO back-powering;
- ring/strap/ear/head fit produces user-specific intermittent data;
- adhesive overflow creates optical leakage, sensor preload, or antenna detuning;
- charger alignment/contact intermittency corrupts charge or data continuity;
- calibration constants mismatch firmware/algorithm/device revision;
- mobile background behavior creates gaps mistaken for sensor failure;
- a polished score hides missing/invalid raw data;
- production yield shifts by supplier lot, finish, dispense station, or size SKU;
- medical-sounding claim exceeds evidence or region authorization;
- head-worn overlay remains visible after tracking loss or wrong-board recognition;
- camera glare/occlusion causes wrong component or probe location;
- voice/gaze command causes an unintended state-changing tool action.

Each case needs exact design/configuration evidence, a measurable symptom, plausible competing hypotheses, safe discriminating experiments, verified root cause, fix, and regression tests.

## 9. Competitive intelligence ownership

| Artifact | Owner | Required reviewers |
|---|---|---|
| Company/product dossier | MKT-02 | SCI-07, META-05, relevant technical agents |
| Feature/spec snapshot | SCI-07 | DOC-02, component/domain specialist |
| Teardown interpretation | owning EE/ME/MFG agent | TEST-04, META-05 |
| Physiological or accuracy claim | SCI-05/10 | REG-03, TEST-13, META-05 |
| XR interface comparison | XR-01/08 | PROD-02, XR-09, SEC-05 |
| Patent mechanism landscape | LEG-02/03 | technical owner, external counsel where required |
| Business-model comparison | BIZ-02/FIN-02 | MKT-01/02, PROD-01 |
| Lab Copilot benchmark conversion | PROD-02 + AI-13 | domain expert, TEST-05, META-06 |

## 10. Refresh cadence and stale-data rules

- Refresh facts before any architecture, procurement, pricing, partner, claim, or competitive decision.
- Maintain product generation and region; never write “Apple Watch,” “Galaxy Watch,” or “Oura” as if every generation is electrically identical.
- Mark mutable facts stale after 90 days for fast-moving product/platform information and after a new generation/OS release.
- Preserve historical snapshots because generation-to-generation changes are valuable debugging and product-strategy evidence.
- Do not overwrite a prior conclusion; supersede it with new evidence and explain what changed.

## 11. Definition of useful competitive knowledge

Competitive knowledge is useful only when it changes an engineering or product action. Every dossier should end with:

```markdown
## Verified product facts
## Vendor claims requiring independent validation
## Architecture inferences and confidence
## Dominant trade-offs
## Failure/return risks to investigate
## What this teaches the Lab Copilot
## Benchmark cases to add
## Build / buy / partner implications
## Unknowns and next evidence to obtain
```

A long list of sensors or features without causal engineering interpretation is not deep expertise.
