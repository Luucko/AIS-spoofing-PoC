import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving plots

df = pd.read_csv("../data/processed/ais_type123_clean.csv")
print(f"Loaded {len(df)} clean records")
df_unfiltered = pd.read_csv("../data/processed/ais_decoded_20260305_2124.csv")
print(f"Loaded {len(df_unfiltered)} unfiltered records")

# 1. Histograms of all 7 features

def plot_histograms(df, title, filename, color):
    features = ['lat', 'lon', 'sog', 'cog', 'heading', 'rot', 'nav_status']
    plt.figure(figsize=(20, 12))
    
    for i, feature in enumerate(features):
        plt.subplot(3, 3, i + 1)
        plt.hist(df[feature], bins=30, alpha=0.7, color=color)
        plt.title(f"{feature} distribution")
        plt.xlabel(feature)
        plt.ylabel("Frequency")
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(filename)
    print(f"Saved histogram plot: {filename}")
    plt.close()

# Plot histograms for unfiltered data — red signals raw/noisy
plot_histograms(df_unfiltered, "Feature Distributions - Unfiltered AIS Data","../data/processed/eda_histograms_unfiltered.png", color='#C0392B')

# Plot histograms for cleaned data — blue signals processed/reliable
plot_histograms(df, "Feature Distributions - Cleaned Type 1/2/3 Position Reports","../data/processed/eda_histograms.png", color='#2E86C1')

