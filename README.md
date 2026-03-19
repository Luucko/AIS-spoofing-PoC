# AIS Spoofing PoC (work in progress)

Proof of Concept for the research paper *"Generative AI as an Enabler of AIS Spoofing: Threat Assessment for North Sea Maritime Cyber-Physical Systems"*, part of the NEPTARGOS project, Fontys ICT Eindhoven.

## What this project does

Tests whether two Generative AI techniques (a GAN and an LLM) can produce realistic spoofed AIS messages for North Sea scenarios. Real AIS data is captured, cleaned, explored, used to train a GAN and prompt an LLM, and the generated output is encoded into valid NMEA 0183 sentences for evaluation.

## Project structure

```
ais-spoofing-poc/
├── data/
│   ├── raw/                                        # Raw NMEA capture files (not in git)
│   │   └── ais_raw_20260305_2124.txt               # Raw capture (12.6h, ~1.84M lines)
│   └── processed/                                  # Decoded, cleaned, and generated data (not in git)
│       ├── ais_decoded_20260305_2124.csv            # Full decoded capture (1,161,491 records)
│       ├── ais_type123_clean.csv                    # Cleaned Type 1/2/3 records (648,253 records)
│       ├── eda_histograms.png                       # Feature distribution histograms (cleaned)
│       ├── eda_histograms_unfiltered.png            # Feature distribution histograms (unfiltered)
│       ├── eda_map.png                              # World map comparison (unfiltered vs cleaned)
│       ├── eda_map_zoomed.png                       # Norwegian coast map comparison
│       └── eda_summary.md                           # Summary statistics table (markdown)
├── notebooks/
│   ├── 01_capture_ais.py                            # Connect to Norwegian AIS feed, capture and decode
│   ├── 02_data_exploration.py                       # Filter and clean decoded data per ITU-R M.1371
│   ├── 03_eda.py                                    # Exploratory Data Analysis: histograms, maps, stats
│   ├── 04_encoder_demo.py                           # Demonstrate pyais encode_dict (fictional vessel)
│   └── 05_train_gan.py                              # GAN training pipeline (in progress)
├── tests/
│   ├── test_decoder.py                              # Validate pyais decoder (incl. third-party verification)
│   └── test_encoder.py                              # Validate pyais encoder (round-trip on real data)
├── src/                                             # Future: LLM comparison, evaluation scripts
├── .gitignore
└── README.md
```

## Pipeline overview

1. **Data Collection**: Capture live AIS data from Norwegian Coastal Administration feed
2. **Data Cleaning**: Filter to Type 1/2/3, remove invalid values per ITU-R M.1371
3. **Exploratory Data Analysis**: Histograms, geographic maps, summary statistics
4. **Encoding Validation**: Validate pyais encoder/decoder via round-trip and third-party testing
5. **GAN Training**: Train tabular MLP-GAN on cleaned AIS data (PyTorch)
6. **LLM Prompting**: Few-shot LLM comparison (Claude/GPT-4 API)
7. **Evaluation**: Compare GAN vs LLM output against real baseline
8. **Scenario Demonstration**: 3 North Sea spoofing scenarios end-to-end

## Data

- **Source:** Norwegian Coastal Administration live AIS feed (153.44.253.27:5631), public open data
- **Captured:** March 5–6, 2026, 12.6 hours
- **Raw:** ~1.84 million lines received, 1,161,491 successfully decoded
- **Cleaned:** 648,253 Type 1/2/3 position reports from 2,739 unique vessels

## Dependencies

```
pip install pyais pandas pytest torch matplotlib geopandas tabulate
```

## How to run

Notebooks run from inside the `notebooks/` folder:
```
cd notebooks
python 01_capture_ais.py
python 02_data_exploration.py
python 03_eda.py
python 04_encoder_demo.py
python 05_train_gan.py
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
| 5 | Train GAN | In progress |
| 6 | LLM comparison | Pending |
| 7 | Encode and evaluate | Pending |
| 8 | Attack scenario demonstrations | Pending |
| 9 | Paper writing (Sections III–VII) | Pending |