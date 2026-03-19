import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving plots

# Load filtered and unfiltered datasets
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


# 2. Geographical map of recorded coordinates

# World view: before and after cleaning side by side
world = gpd.read_file("https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip")
fig, axes = plt.subplots(1, 2, figsize=(22, 8))

def plot_map(df, df_label, filename, color, extent=None):
    fig, ax = plt.subplots(figsize=(14, 10))
    world.plot(ax=ax, color='#E8E8E8', edgecolor='#B0B0B0', linewidth=0.5)
    ax.scatter(df['lon'], df['lat'], s=0.05, alpha=0.3, color=color)
    ax.set_title(df_label, fontsize=14, fontweight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    
    if extent:
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])
    
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"Saved map: {filename}")
    plt.close()

# Unfiltered
world.plot(ax=axes[0], color='#E8E8E8', edgecolor='#B0B0B0', linewidth=0.5)
axes[0].scatter(df_unfiltered['lon'], df_unfiltered['lat'], s=0.05, alpha=0.3, color='#C0392B')
axes[0].set_title('Positions — Unfiltered Data', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')
axes[0].grid(True, alpha=0.2)

# Cleaned
world.plot(ax=axes[1], color='#E8E8E8', edgecolor='#B0B0B0', linewidth=0.5)
axes[1].scatter(df['lon'], df['lat'], s=0.05, alpha=0.3, color='#2E86C1')
axes[1].set_title('Positions — Cleaned Type 1/2/3 Data', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Longitude')
axes[1].set_ylabel('Latitude')
axes[1].grid(True, alpha=0.2)

plt.suptitle('Geographic Distribution of AIS Records', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig("../data/processed/eda_map.png", dpi=150)
print("Saved map: eda_map.png")
plt.close()

# Zoomed-in Norway: before and after cleaning side by side
fig, axes = plt.subplots(1, 2, figsize=(22, 8))

# Unfiltered
world.plot(ax=axes[0], color='#E8E8E8', edgecolor='#B0B0B0', linewidth=0.5)
axes[0].scatter(df_unfiltered['lon'], df_unfiltered['lat'], s=0.1, alpha=0.3, color='#C0392B')
axes[0].set_title('Positions — Unfiltered Data', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')
axes[0].set_xlim(-5, 35)
axes[0].set_ylim(54, 75)
axes[0].grid(True, alpha=0.2)

# Cleaned — zoomed
world.plot(ax=axes[1], color='#E8E8E8', edgecolor='#B0B0B0', linewidth=0.5)
axes[1].scatter(df['lon'], df['lat'], s=0.1, alpha=0.3, color='#2E86C1')
axes[1].set_title('Positions — Cleaned Type 1/2/3 Data', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Longitude')
axes[1].set_ylabel('Latitude')
axes[1].set_xlim(-5, 35)
axes[1].set_ylim(54, 75)
axes[1].grid(True, alpha=0.2)

plt.suptitle('Geographic Distribution of AIS Records — Norwegian Coast', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig("../data/processed/eda_map_zoomed.png", dpi=150)
print("Saved map: eda_map_zoomed.png")
plt.close()


# 3. Summary statistics table

features = ['lat', 'lon', 'sog', 'cog', 'heading', 'rot', 'nav_status']
df_unfiltered_pos = df_unfiltered[df_unfiltered["msg_type"].isin([1, 2, 3])]

with open("../data/processed/eda_summary.md", "w") as f:
    def write(line=""):
        f.write(line + "\n")

    write(f"# EDA Summary\n")

    write(f"## Unfiltered Type 1/2/3 Data ({len(df_unfiltered_pos)} records, {df_unfiltered_pos['mmsi'].nunique()} vessels)\n")
    write(df_unfiltered_pos[features].describe().round(4).to_markdown())

    write(f"\n## Cleaned Type 1/2/3 Data ({len(df)} records, {df['mmsi'].nunique()} vessels)\n")
    write(df[features].describe().round(4).to_markdown())

    write(f"\n## Key Observations\n")
    write(f"| Metric | Value |")
    write(f"|--------|-------|")
    write(f"| Records removed by cleaning | {len(df_unfiltered_pos) - len(df)} ({(len(df_unfiltered_pos) - len(df)) / len(df_unfiltered_pos) * 100:.1f}%) |")
    write(f"| Vessels removed by cleaning | {df_unfiltered_pos['mmsi'].nunique() - df['mmsi'].nunique()} |")
    write(f"| Stationary vessels (SOG=0) | {(df['sog'] == 0).sum()} ({(df['sog'] == 0).sum() / len(df) * 100:.1f}%) |")
    write(f"| Nav status 0 (under way) | {(df['nav_status'] == 0).sum()} ({(df['nav_status'] == 0).sum() / len(df) * 100:.1f}%) |")
    write(f"| Nav status 5 (moored) | {(df['nav_status'] == 5).sum()} ({(df['nav_status'] == 5).sum() / len(df) * 100:.1f}%) |")
    write(f"| Nav status 15 (undefined) | {(df['nav_status'] == 15).sum()} ({(df['nav_status'] == 15).sum() / len(df) * 100:.1f}%) |")

print("Saved summary: eda_summary.md")