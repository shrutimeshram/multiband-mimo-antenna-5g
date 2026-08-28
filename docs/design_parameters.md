# Design parameters and rationale

## Substrate

| Parameter | Value | Why |
|---|---|---|
| Material | FR4 (lossy) | Cheap and universally available; the standard choice for a student prototype where fabrication cost matters more than loss tangent |
| Relative permittivity (εr) | 4.3 | Sets the effective wavelength, and therefore patch size, for a given resonant frequency |
| Dimensions | 130 × 74 × 1.6 mm | 1.6 mm is standard PCB thickness; the board area accommodates four elements with enough separation to keep coupling manageable |
| Conductor | Copper / PEC | Low cost, ductile, high conductivity |

## Radiating element

| Parameter | Value |
|---|---|
| Patch dimensions | 21 × 18 × 0.035 mm |
| Geometry | Rectangular microstrip patch with an L-slot |
| Feed | Microstrip line |
| Elements | 4 (MIMO array) |

### Why an L-slot

A plain rectangular patch resonates at a single frequency set by its length. Cutting an
**L-shaped slot** into the patch forces the surface current to travel around the slot,
lengthening the effective electrical path without enlarging the physical patch. That
introduces additional resonances, turning a single-band radiator into a multi-band one
inside the same footprint — which is the constraint that matters in a handset.

### Why a defected ground structure

Four elements on one small board couple to each other through the shared ground plane.
Etching a **defected ground structure (DGS)** between elements interrupts those surface
currents, suppressing mutual coupling (S21) without needing extra board area.

## Design progression

The thesis works through three stages, each simulated and characterised in CST:

1. **Single antenna element** — establish the baseline resonance, VSWR, impedance, gain and
   directivity for one L-slot patch.
2. **Four-element MIMO array** — replicate the element, then measure the transmission
   coefficient (S21) to quantify how badly the elements interfere.
3. **MIMO array with DGS** — add the ground-plane defect and re-measure, confirming the
   isolation improvement.

## Results achieved

| Band | Coverage | Centre | S11 |
|---|---|---|---|
| 1 | 3.28 – 3.72 GHz | 3.416 GHz | −21.815 dB |
| 2 | 4.33 – 5.25 GHz | 5.040 GHz | −32.345 dB |
| 3 | 5.81 – 6.00 GHz | 5.896 GHz | −14.114 dB |

**ECC < 0.1** across the operating bands, against an acceptance threshold of 0.5.

## Parameters characterised

- S-parameters — reflection coefficient (S11) and transmission coefficient (S21)
- VSWR
- Input impedance
- Mutual coupling between elements
- Gain (2D and 3D)
- Directivity
- Radiation pattern
- Surface current distribution and H-field
- Radiation, total and antenna efficiency
- Envelope correlation coefficient

## Target applications

5G NR sub-6 GHz, Wi-Fi, WiMAX and WLAN.
