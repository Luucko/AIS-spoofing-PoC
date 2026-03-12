from pyais import decode
from pyais.encode import encode_dict

# ============================================================
# Demo: Encode a realistic North Sea vessel, then decode it
# ============================================================

# A fictional Dutch cargo vessel approaching the Port of Rotterdam
vessel_data = {
    'type': 1,
    'mmsi': '244670316',       # Dutch MMSI prefix (244)
    'status': 0,               # Under way using engine
    'turn': -3.0,              # Slight left turn
    'speed': 14.2,             # 14.2 knots
    'accuracy': 1,             # High accuracy GPS
    'lon': 4.0021,             # Approaching Rotterdam from the west
    'lat': 51.9850,            # North Sea, near Hook of Holland
    'course': 95.5,            # Heading roughly east into port
    'heading': 97,
    'second': 42,
    'maneuver': 0,
    'raim': 0,
}

print("INPUT: Fictional Dutch cargo vessel near Rotterdam")
print(f"  MMSI:    {vessel_data['mmsi']}")
print(f"  Lat:     {vessel_data['lat']}")
print(f"  Lon:     {vessel_data['lon']}")
print(f"  SOG:     {vessel_data['speed']} knots")
print(f"  COG:     {vessel_data['course']} degrees")
print(f"  Heading: {vessel_data['heading']} degrees")
print(f"  ROT:     {vessel_data['turn']}")
print(f"  Status:  {vessel_data['status']} (under way using engine)")

# Encode
encoded = encode_dict(vessel_data)
print(f"\nENCODED NMEA SENTENCE:")
print(f"  {encoded[0]}")

# Decode it back
decoded = decode(*encoded).asdict()
print(f"\nDECODED BACK:")
print(f"  MMSI:    {decoded['mmsi']}")
print(f"  Lat:     {decoded['lat']}")
print(f"  Lon:     {decoded['lon']}")
print(f"  SOG:     {decoded['speed']} knots")
print(f"  COG:     {decoded['course']} degrees")
print(f"  Heading: {decoded['heading']} degrees")
print(f"  ROT:     {decoded['turn']}")
print(f"  Status:  {decoded['status']} (under way using engine)")

# Verify
print(f"\nROUND-TRIP VERIFICATION:")
print(f"  MMSI match:    {str(decoded['mmsi']) == vessel_data['mmsi']}")
print(f"  SOG match:     {decoded['speed'] == vessel_data['speed']}")
print(f"  COG match:     {decoded['course'] == vessel_data['course']}")
print(f"  Heading match: {decoded['heading'] == vessel_data['heading']}")
print(f"  Lat diff:      {abs(decoded['lat'] - vessel_data['lat']):.6f} degrees")
print(f"  Lon diff:      {abs(decoded['lon'] - vessel_data['lon']):.6f} degrees")