# AIS Spoofing PoC (work in progress)

Proof of Concept for the research paper *"Generative AI as an Enabler of AIS Spoofing: Threat Assessment for North Sea Maritime Cyber-Physical Systems"*, part of the NEPTARGOS project, Fontys ICT Eindhoven.

## What this project does

Tests whether two Generative AI techniques (a GAN and an LLM) can produce realistic spoofed AIS messages for North Sea scenarios. Real AIS data is captured, cleaned, used to train a GAN and prompt an LLM, and the generated output is encoded into valid NMEA 0183 sentences for evaluation.

## Project structure

```
ais-spoofing-poc/
├── data/
│   ├── raw/                    # Raw NMEA capture files (not in git)
│   |   └── ais_raw_20260305_2124.txt       # Raw capture
│   └── processed/              # Decoded and cleaned CSVs (not in git)
│       ├── ais_decoded_20260305_2124.csv   # Full decoded capture
│       └── ais_type123_clean.csv           # Cleaned Type 1/2/3 records
├── notebooks/
│   ├── 01_capture_ais.py       # Connects to Norwegian AIS feed, captures and decodes live data
│   ├── 02_data_exploration.py  # Filters and cleans decoded data per ITU-R M.1371
│   └── 03_encoder_demo.py      # Demonstrates pyais encode_dict with a fictional North Sea vessel
├── tests/
│   ├── test_decoder.py         # Validates pyais decoder against known values and third-party decoder
│   └── test_encoder.py         # Validates pyais encoder via round-trip testing on real captured data
├── src/                        # GAN and LLM generation scripts (upcoming)
├── .gitignore
└── README.md
```

## Data

Source: Norwegian Coastal Administration live AIS feed (153.44.253.27:5631), public open data.
Captured on March 5–6, 2026 over 12.6 hours. ~1.84 million lines received, 1,161,491 decoded.
After filtering to Type 1/2/3 position reports and removing invalid values per ITU-R M.1371: 648,253 clean records from 2,739 unique vessels.

## Dependencies

```
pip install pyais pandas pytest torch
```

- **pyais**: AIS decoding and encoding (NMEA 0183 / ITU-R M.1371)
- **pandas**: Data handling and CSV processing
- **pytest**: Test framework
- **torch**: PyTorch for GAN training (upcoming)

## How to run

Notebooks run from inside the `notebooks/` folder:
```
cd notebooks
python 01_capture_ais.py
python 02_data_exploration.py
python 03_encoder_demo.py
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
| 3 | Validate NMEA encoder/decoder | Done (28/28 tests passing) |
| 4 | Train GAN | Next |
| 5 | LLM comparison | Pending |
| 6 | Encode and evaluate | Pending |
| 7 | Attack scenario demonstrations | Pending |
| 8 | Paper writing (Sections III–VII) | Pending |