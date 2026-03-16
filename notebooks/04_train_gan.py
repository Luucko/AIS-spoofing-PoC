import pandas as pd
import torch
import numpy as np


# Step 1: Load and prepare data.

df = pd.read_csv("../data/processed/ais_type123_clean.csv")
print(f"Loaded {len(df)} records")

# Select only the fields the GAN will learn from => No timestamp, no MMSI, no msg_type because not interesting for GAN to learn.
features = ['lat', 'lon', 'sog', 'cog', 'heading', 'rot', 'nav_status']
data = df[features].copy()

print(f"Selected {len(features)} features: {features}")
print(f"\nRaw data statistics:")
print(data.describe().round(4))     # With pandas 2.0+, you can print data statistics using .describe()


# Step 2: Normalize to [0, 1]

# Step 3: Define the generator.

# Step 4: Define the discriminator.

# Step 5: Training loop.

# Step 6: Generate samples (Print output to data/processed/gan_generated_ais.csv).

# Step 7: Quick sanity check.
