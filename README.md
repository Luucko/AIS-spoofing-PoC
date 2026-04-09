# AIS Spoofing PoC

Proof of Concept for the research paper *"Towards Generative AI-Enabled AIS Spoofing: Data Foundation for Threat Assessment in North Sea Maritime Cyber-Physical Systems"* (Viaene et al., 2026), part of the [NEPTARGOS](https://www.nwo.nl/projecten/cqgmv68308) project at Fontys ICT, Eindhoven.

> **Disclaimer:** This project is conducted entirely in software for academic research purposes. No radio-frequency transmission was performed and no messages were injected into any live AIS system.

## Overview

This repository establishes the data foundation for investigating whether Generative AI techniques can produce realistic spoofed AIS messages for North Sea maritime scenarios. The pipeline captures real AIS data from a live feed, cleans and filters it per ITU-R M.1371 sentinel value definitions, conducts exploratory data analysis to establish empirical traffic baselines, validates a round-trip encoding/decoding pipeline, and demonstrates manual spoofing scenarios targeting Dutch North Sea critical infrastructure.

This work constitutes the first semester (S1) of a two-semester investigation. The second semester will extend the pipeline with tabular GAN training, LLM-based field value generation, and statistical evaluation of synthetic outputs against the baselines established here.

## Pipeline

| Step | Script | Description |
|------|--------|-------------|
| 1 | `01_capture_ais.py` | Connect to Norwegian Coastal Administration live AIS feed, capture and decode NMEA messages in real time |
| 2 | `02_data_cleaning.py` | Filter to Type 1/2/3 position reports, remove records with ITU-R M.1371 sentinel values |
| 3 | `03_eda.ipynb` | Exploratory Data Analysis: field distribution histograms, geographic scatter plots, summary statistics |
| 4 | `04_encoder_demo.py` | Demonstrate pyais `encode_dict` with round-trip encode-decode validation |
| 5 | `05_spoofing_scenarios.ipynb` | Construct and verify four manual spoofing scenarios for Dutch North Sea waters |

## Dataset

| Metric | Value |
|--------|-------|
| Source | Norwegian Coastal Administration ([Kystverket](https://www.kystverket.no/en/sea-transport-and-ports/ais/access-to-ais-data/)) live AIS feed, public open data |
| Capture period | March 5–6, 2026 (12.6 hours) |
| Raw NMEA lines received | ~1.84 million |
| Successfully decoded records | 1,161,491 (across 9 message types) |
| Cleaned Type 1/2/3 records | 648,253 (from 2,739 unique vessels) |
| Records removed by cleaning | 247,259 (27.6%) |

Data files are not included in the repository due to size. To reproduce, run the pipeline scripts in order starting from `01_capture_ais.py`.

## Spoofing Scenarios

Four scenarios were constructed targeting distinct categories of North Sea critical infrastructure, each producing a structurally valid NMEA 0183 sentence verified through round-trip decoding:

| Scenario | Target | Message Type | Flag | Round-Trip |
|----------|--------|:---:|------|:---:|
| Ghost vessel at Maeslantkering | Nieuwe Waterweg / Port of Rotterdam | 1 | NL | PASS |
| Collision threat in wind farm | Hollandse Kust Zuid | 1 | DE | PASS |
| Deceptive presence near subsea cables | Borssele wind farm zone | 1 | RU | PASS |
| Fake Aid-to-Navigation | IJmuiden approach lane | 21 | NL | PASS |

## Project Structure

```
ais-spoofing-poc/
├── data/
│   ├── processed/                                   # Decoded, cleaned, and generated data (not in git)
│   │   ├── ais_decoded_20260305_2124.csv            # Full decoded capture (1,161,491 records)
│   │   ├── ais_type123_clean.csv                    # Cleaned Type 1/2/3 records (648,253 records)
│   │   ├── eda_histograms.png                       # Feature distribution histograms (cleaned)
│   │   ├── eda_histograms_unfiltered.png            # Feature distribution histograms (unfiltered)
│   │   ├── eda_map.png                              # World map comparison (unfiltered vs cleaned)
│   │   ├── eda_map_zoomed.png                       # Norwegian coast map comparison
│   │   └── eda_summary.md                           # Summary statistics table (markdown)
│   └── raw/                                         # Raw NMEA capture files (not in git)
│       └── ais_raw_20260305_2124.txt                # Raw capture (12.6h, ~1.84M lines)
├── notebooks/
│   ├── 01_capture_ais.py                            # Live AIS capture and decoding
│   ├── 02_data_cleaning.py                          # ITU-R M.1371 sentinel value filtering
│   ├── 03_eda.ipynb                                 # Exploratory Data Analysis
│   ├── 04_encoder_demo.py                           # Encoder proof-of-concept
│   └── 05_spoofing_scenarios.ipynb                  # Manual spoofing demonstrations
├── tests/
│   ├── test_decoder.py                              # Decoder validation (incl. !BSVDM prefix, third-party cross-check)
│   └── test_encoder.py                              # Encoder validation (round-trip on 20 real records)
├── .gitignore
└── README.md
```

## Dependencies

```bash
pip install pyais pandas pytest matplotlib geopandas tabulate
```

## Usage

Run notebooks from inside the `notebooks/` directory:

```bash
cd notebooks
python 01_capture_ais.py
python 02_data_cleaning.py
jupyter notebook 03_eda.ipynb
python 04_encoder_demo.py
jupyter notebook 05_spoofing_scenarios.ipynb
```

Run tests from the project root:

```bash
pytest tests/ -v
```

All 28 tests should pass, covering decoder correctness, encoder field preservation, and round-trip validation on real dataset records.

## Validation

| Category | Tests | Status |
|----------|:---:|:---:|
| Decoder (incl. !BSVDM prefix) | 4 | PASS |
| Encoder (field-by-field) | 4 | PASS |
| Round-trip (20 real records) | 20 | PASS |
| **Total** | **28** | **28/28** |

Latitude and longitude values are verified within a tolerance of 0.001°, consistent with the 1/10,000-minute precision of ITU-R M.1371 encoding. Decoder output was additionally cross-verified against the [aggsoft.com AIS decoder](https://www.aggsoft.com/ais-decoder.htm).

## Citation

If you use this work, please cite:

```
L. Viaene, F. Ousta, N. Kuijpers, and C. Schellekens, "Towards Generative AI-Enabled
AIS Spoofing: Data Foundation for Threat Assessment in North Sea Maritime Cyber-Physical
Systems," Fontys ICT, Eindhoven, 2026.
```

## Licence

This project is developed for academic research within the NEPTARGOS project, funded by the Dutch Research Council (NWO).