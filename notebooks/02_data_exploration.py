import pandas as pd

# Load the decoded data
df = pd.read_csv("../data/processed/ais_decoded_20260305_2124.csv")

# Basic overview
print(f"Total records: {len(df)}")
print(f"\nMessage types captured:")
print(df["msg_type"].value_counts())

# Print ranges of key fields
def print_ranges(df, title):
    print(f"\n--- Ranges {title} ---")
    print(f"Unique vessels (MMSI): {df['mmsi'].nunique()}")
    print(f"Latitude range: {df['lat'].min():.4f} to {df['lat'].max():.4f}")
    print(f"Longitude range: {df['lon'].min():.4f} to {df['lon'].max():.4f}")
    print(f"SOG range: {df['sog'].min()} to {df['sog'].max()} knots")
    print(f"COG range: {df['cog'].min()} to {df['cog'].max()}")
    print(f"Heading range: {df['heading'].min()} to {df['heading'].max()}")
    print(f"ROT range: {df['rot'].min()} to {df['rot'].max()}")
    print(f"NAV Status range: {df['nav_status'].min()} to {df['nav_status'].max()}")

# Ranges before cleaning
print_ranges(df, "BEFORE Cleaning")

# Filter for Type 1, 2, 3 only (Class A position reports - our GAN training data)
pos_reports = df[df["msg_type"].isin([1, 2, 3])].copy()
print(f"\nType 1/2/3 position reports (before cleaning): {len(pos_reports)}")

# Remove invalid/unavailable values per ITU-R M.1371
pos_reports = pos_reports[
    (pos_reports["lat"] >= -90) & (pos_reports["lat"] <= 90) &              # valid latitude range
    (pos_reports["lat"] != 91.0) &                                          # 91 = not available
    (pos_reports["lon"] >= -180) & (pos_reports["lon"] <= 180) &            # valid longitude range
    (pos_reports["lon"] != 181.0) &                                         # 181 = not available
    (pos_reports["sog"] <= 102.2) &                                         # 102.2+ = not available
    (pos_reports["cog"] < 360.0) &                                          # 360 = not available
    (pos_reports["heading"] < 360.0) &                                      # 360+ = invalid/not available
    (pos_reports["rot"] >= -127) & (pos_reports["rot"] <= 127) &            # -128 = not available
    (pos_reports["nav_status"] >= 0) & (pos_reports["nav_status"] <= 15)    # 0-15 = valid range
]

print(f"Type 1/2/3 position reports (after cleaning): {len(pos_reports)}")

# Ranges after cleaning
print_ranges(pos_reports, "AFTER Cleaning")


# Save the cleaned dataset
pos_reports.to_csv("../data/processed/ais_type123_clean.csv", index=False)
print(f"\nSaved {len(pos_reports)} clean position reports to data/processed/ais_type123_clean.csv")