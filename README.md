# Multi-band MIMO Antenna for 5G Wireless Applications

Design and simulation of a **four-element multi-band MIMO antenna** for 5G, Wi-Fi, WiMAX and
WLAN bands, modelled in **CST Studio Suite**.

Published as *"Design of Multi-band MIMO Antenna for 5G Wireless Applications"* at
**ICICICT 2022** — the 3rd International Conference on Intelligent Computing, Instrumentation
and Control Technologies, held at Vimal Jyothi Engineering College, Kannur, Kerala, India,
11–12 August 2022 (Paper ID 696).

Undertaken as the final-year B.E. project in Electronics & Telecommunication Engineering at
**Yeshwantrao Chavan College of Engineering, Nagpur**.

---

## Design

| Parameter | Value |
|---|---|
| Elements | 4 radiating elements (MIMO) |
| Substrate | FR4 (lossy), εr = 4.3 |
| Substrate dimensions | 130 × 74 × 1.6 mm |
| Patch dimensions | 21 × 18 × 0.035 mm |
| Ground & patch material | PEC / copper |
| Feed | Microstrip line |
| Slot geometry | L-slot in a rectangular microstrip patch |
| Simulation tool | CST Studio Suite |

The **L-slot** is what turns a single-resonance rectangular patch into a multi-band radiator —
it lengthens the effective current path without enlarging the patch footprint, adding
resonances rather than shifting the existing one.

A **defected ground structure (DGS)** variant was also developed to reduce mutual coupling
between adjacent elements; the design progression (single element → 4-element MIMO →
MIMO with DGS) is documented in the thesis.

## Results

Three operating bands were achieved:

| Band | Coverage | Centre frequency | Reflection coefficient (S11) |
|---|---|---|---|
| Band 1 | 3.28 – 3.72 GHz | 3.416 GHz | −21.815 dB |
| Band 2 | 4.33 – 5.25 GHz | 5.040 GHz | −32.345 dB |
| Band 3 | 5.81 – 6.00 GHz | 5.896 GHz | −14.114 dB |

Applications covered: **5G NR (n78 / sub-6 GHz)**, **Wi-Fi**, **WiMAX** and **WLAN**.

**Envelope Correlation Coefficient (ECC) < 0.1** across the operating bands — comfortably
inside the ECC < 0.5 threshold generally required for usable MIMO diversity performance.

Parameters characterised: S-parameters (reflection and transmission coefficients), VSWR,
input impedance, mutual coupling, gain, directivity, radiation pattern, surface current
distribution and radiation efficiency.

## Repository layout

```
analysis/
  plot_s_parameters.py   -- plot S11/S21 from CST-exported data, mark -10 dB bandwidth
  compute_ecc.py         -- envelope correlation coefficient from S-parameters
data/
  (export your CST touchstone / CSV results here)
docs/
  design_parameters.md   -- full dimension table and design rationale
```

## Running the analysis scripts

```bash
pip install -r requirements.txt

# S-parameter plot with automatic -10 dB bandwidth annotation
python analysis/plot_s_parameters.py --data data/s_parameters.csv

# ECC computed from the S-parameter matrix
python analysis/compute_ecc.py --data data/s_parameters.csv
```

Both scripts read a CSV exported from CST with a `frequency` column (GHz) plus
S-parameter columns in dB (`S11`, `S21`, …) or as complex values.

## Publication

> S. Meshram, A. Mandhalkar, I. Shival, *"Design of Multi-band MIMO Antenna for 5G Wireless
> Applications"*, 3rd International Conference on Intelligent Computing, Instrumentation and
> Control Technologies (ICICICT), Kannur, Kerala, India, August 2022.

Project guide: Dr. Sachin S. Khade · Co-guide: Dr. P. S. Ashtankar
