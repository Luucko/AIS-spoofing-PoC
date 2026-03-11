import pandas as pd

# Load the decoded data
df = pd.read_csv("../data/processed/ais_decoded_20260305_2124.csv")

# Basic overview
print(f"Total records: {len(df)}")
print(f"\nMessage types captured:")
print(df["msg_type"].value_counts())

# Filter for Type 1, 2, 3 only (Class A position reports - our GAN training data)
pos_reports = df[df["msg_type"].isin([1, 2, 3])].copy()
print(f"\nType 1/2/3 position reports (before cleaning): {len(pos_reports)}")

# Remove invalid/unavailable values per ITU-R M.1371
pos_reports = pos_reports[
    (pos_reports["lat"] >= -90) & (pos_reports["lat"] <= 90) &    # valid latitude range
    (pos_reports["lat"] != 91.0) &                                 # 91 = not available
    (pos_reports["lon"] >= -180) & (pos_reports["lon"] <= 180) &  # valid longitude range
    (pos_reports["lon"] != 181.0) &                                # 181 = not available
    (pos_reports["sog"] <= 102.2) &                                # 102.2+ = not available
    (pos_reports["cog"] < 360.0) &                                 # 360 = not available
    (pos_reports["heading"] < 360.0) &                             # 360+ = invalid/not available
    (pos_reports["rot"] >= -127) & (pos_reports["rot"] <= 127) &  # -128 = not available
    (pos_reports["nav_status"] >= 0) & (pos_reports["nav_status"] <= 15)  # 0-15 = valid range
]

print(f"Type 1/2/3 position reports (after cleaning): {len(pos_reports)}")

# Stats after cleaning
print(f"\n--- Clean Position Report Statistics ---")
print(f"Unique vessels (MMSI): {pos_reports['mmsi'].nunique()}")
print(f"Latitude range: {pos_reports['lat'].min():.4f} to {pos_reports['lat'].max():.4f}")
print(f"Longitude range: {pos_reports['lon'].min():.4f} to {pos_reports['lon'].max():.4f}")
print(f"SOG range: {pos_reports['sog'].min()} to {pos_reports['sog'].max()} knots")
print(f"COG range: {pos_reports['cog'].min()} to {pos_reports['cog'].max()}")
print(f"Heading range: {pos_reports['heading'].min()} to {pos_reports['heading'].max()}")
print(f"ROT range: {pos_reports['rot'].min()} to {pos_reports['rot'].max()}")
print(f"NAV Status range: {pos_reports['nav_status'].min()} to {pos_reports['nav_status'].max()}")


# Save the cleaned dataset
pos_reports.to_csv("../data/processed/ais_type123_clean.csv", index=False)
print(f"\nSaved {len(pos_reports)} clean position reports to data/processed/ais_type123_clean.csv")