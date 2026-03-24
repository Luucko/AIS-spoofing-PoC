import pandas as pd
import torch
import numpy as np


# 1: Load and prepare data.

df = pd.read_csv("../data/processed/ais_type123_clean.csv")
print(f"Loaded {len(df)} records")

# Select only the fields the GAN will learn from => No timestamp, no MMSI, no msg_type because not interesting for GAN to learn.
features = ['lat', 'lon', 'sog', 'cog', 'heading', 'rot', 'nav_status']
data = df[features].copy()

print(f"Selected {len(features)} features: {features}")
print(f"\nData statistics:")
print(data.describe().round(4))     # With pandas 2.0+, you can print data statistics using .describe()


# 2: Normalize to [0, 1]

data_min = data.min()       # Store min for each field (needed later to convert back)
data_max = data.max()       # Store max for each field

data_normalized = (data - data_min) / (data_max - data_min)     # Manual min-max normalization for transparency (instead of using sklearn's MinMaxScaler) 
# from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler()
# data_normalized = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

print(f"\nNormalized data statistics:")
print(data_normalized.describe().round(4))

# Convert to PyTorch tensor
tensor_data = torch.FloatTensor(data_normalized.values.copy())
print(f"\nPyTorch tensor shape: {tensor_data.shape}")
print(f"This means: {tensor_data.shape[0]} records, each with {tensor_data.shape[1]} features")

# Quick test: denormalize one sample to verify we can reverse the process
sample_normalized = tensor_data[0].numpy()
sample_original = sample_normalized * (data_max.values - data_min.values) + data_min.values

print(f"\n--- Denormalization verification ---")
print(f"First record from CSV:        {df[features].iloc[0].values}")
print(f"First record normalized:      {np.round(sample_normalized, 4)}")
print(f"After normalize+denormalize:   {sample_original.round(4)}")
print(f"Match: {np.allclose(df[features].iloc[0].values, sample_original, atol=0.001)}")


# 3: Define the generator.

# 4: Define the discriminator.

# 5: Training loop.

# 6: Generate samples (Print output to data/processed/gan_generated_ais.csv).

# 7: Quick sanity check.
