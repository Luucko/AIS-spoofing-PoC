# AIS Spoofing PoC

Proof of Concept for the research paper *"Towards Generative AI-Enabled AIS Spoofing: Data Foundation for Threat Assessment in North Sea Maritime Cyber-Physical Systems"*, part of the NEPTARGOS project, Fontys ICT Eindhoven.

## What this project does

Establishes the data foundation for investigating whether Generative AI techniques can produce realistic spoofed AIS messages for North Sea scenarios. Real AIS data is captured from a live feed, cleaned and filtered per ITU-R M.1371 standards, explored through statistical and geographic analysis, and validated through a round-trip encoding/decoding pipeline. Manual spoofing scenarios demonstrate that structurally valid and contextually plausible AIS messages can be constructed for Dutch North Sea waters.

This repository represents the first semester of a two-semester investigation within the NEPTARGOS project.

## Project structure

```
ais-spoofing-poc/
├── data/
│   ├── processed/                                   # Decoded, cleaned, and generated data (not in git)
│   |   ├── ais_decoded_20260305_2124.csv            # Full decoded capture (1,161,491 records)
│   |   ├── ais_type123_clean.csv                    # Cleaned Type 1/2/3 records (648,253 records)
│   |   ├── eda_histograms.png                       # Feature distribution histograms (cleaned)
│   |   ├── eda_histograms_unfiltered.png            # Feature distribution histograms (unfiltered)
│   |   ├── eda_map.png                              # World map comparison (unfiltered vs cleaned)
│   |   ├── eda_map_zoomed.png                       # Norwegian coast map comparison
│   |   └── eda_summary.md                           # Summary statistics table (markdown)
│   └── raw/                                         # Raw NMEA capture files (not in git)
│       └── ais_raw_20260305_2124.txt                # Raw capture (12.6h, ~1.84M lines)
├── notebooks/
│   ├── 01_capture_ais.py                            # Connect to Norwegian AIS feed, capture and decode
│   ├── 02_data_cleaning.py                          # Filter and clean decoded data per ITU-R M.1371
│   ├── 03_eda.py                                    # Exploratory Data Analysis: histograms, maps, stats
│   ├── 04_encoder_demo.py                           # Demonstrate pyais encode_dict (round-trip validation)
│   └── 05_spoofing_scenarios.py                     # Manual spoofing scenarios for Dutch North Sea waters
├── tests/
│   ├── test_decoder.py                              # Validate pyais decoder (incl. third-party verification)
│   └── test_encoder.py                              # Validate pyais encoder (round-trip on real data)
├── .gitignore
└── README.md
```

## Pipeline overview

1. **Data Collection**: Capture live AIS data from Norwegian Coastal Administration feed
2. **Data Cleaning**: Filter to Type 1/2/3 position reports, remove invalid values per ITU-R M.1371
3. **Exploratory Data Analysis**: Histograms, geographic maps, summary statistics
4. **Encoding Validation**: Validate pyais encoder/decoder via round-trip and third-party testing (28/28 tests passing)
5. **Manual Spoofing Scenarios**: Construct spoofed AIS messages for Dutch North Sea scenarios using validated encoder

## Data

- **Source:** Norwegian Coastal Administration live AIS feed (153.44.253.27:5631), public open data
- **Captured:** March 5–6, 2026, 12.6 hours
- **Raw:** ~1.84 million lines received, 1,161,491 successfully decoded
- **Cleaned:** 648,253 Type 1/2/3 position reports from 2,739 unique vessels

## Dependencies

```
pip install pyais pandas pytest matplotlib geopandas tabulate
```

## How to run

Notebooks run from inside the `notebooks/` folder:
```
cd notebooks
python 01_capture_ais.py
python 02_data_cleaning.py
python 03_eda.py
python 04_encoder_demo.py
python 05_spoofing_scenarios.py
```

Tests run from the project root:
```
pytest tests/ -v
```

## Current status

| Step | Description | Status |
|------|-------------|--------|
| 1 | Capture live AIS data | Done |
| 2 | Clean and filter dataset | Done |
| 3 | Exploratory Data Analysis | Done |
| 4 | Validate NMEA encoder/decoder | Done (28/28 tests passing) |
| 5 | Manual spoofing scenarios | Done |