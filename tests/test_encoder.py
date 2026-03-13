import pytest
from pyais import decode
from pyais.encode import encode_dict
import pandas as pd


class TestBasicEncode:
    """Test that pyais encode_dict produces valid NMEA sentences from field values."""

    def setup_method(self):
        """Define test input used across basic encode tests."""
        self.input_data = {
            'type': 1,              # AIS message type 1 = position report
            'mmsi': '259366000',    # MMSI number
            'status': 0,            # Under way using engine
            'turn': 0.0,            # Not turning
            'speed': 12.5,          # 12.5 knots over ground
            'accuracy': 0,          # Low accuracy GPS
            'lon': 7.510365,        # Longitude near Bergen, Norway
            'lat': 63.046247,       # Latitude near Bergen, Norway
            'course': 48.1,         # 48.1 degrees true course over ground
            'heading': 247,         # 247 degrees true heading
            'second': 30,           # AIS position report at 30 seconds past the minute
            'maneuver': 0,          # Not engaged in maneuver
            'raim': 0,              # RAIM not in use
        }
        self.encoded = encode_dict(self.input_data)
        self.decoded = decode(*self.encoded).asdict()   # Decoder validated in test_decoder.py

    def test_encoded_is_not_empty(self):
        assert len(self.encoded) > 0

    def test_encoded_is_valid_ais_sentence(self):
        assert self.encoded[0].startswith("!AIVDM") or self.encoded[0].startswith("!AIVDO") # !AIVDO is used for AIS messages from own create ship (e.g. for testing)

    def test_mmsi_matches(self):
        assert str(self.decoded['mmsi']) == self.input_data['mmsi']

    def test_sog_matches(self):
        assert self.decoded['speed'] == self.input_data['speed']

    def test_cog_matches(self):
        assert self.decoded['course'] == self.input_data['course']

    def test_heading_matches(self):
        assert self.decoded['heading'] == self.input_data['heading']

    def test_status_matches(self):
        assert self.decoded['status'] == self.input_data['status']

    def test_lat_within_tolerance(self):
        assert abs(self.decoded['lat'] - self.input_data['lat']) < 0.001     # AIS resolution is 1/10000 minute ≈ 0.000167 degrees

    def test_lon_within_tolerance(self):
        assert abs(self.decoded['lon'] - self.input_data['lon']) < 0.001


class TestRoundTrip:
    """Round-trip test: take real captured data, encode it, decode it, compare."""

    def setup_method(self):
        """Load a sample of real captured AIS data."""
        self.df = pd.read_csv("data/processed/ais_type123_clean.csv")
        self.sample = self.df.head(20)      # Test on first 20 rows

    def _round_trip(self, row):
        """Encode a row from the CSV, decode the result, return both."""
        input_data = {
            'type': int(row['msg_type']),
            'mmsi': str(int(row['mmsi'])),
            'speed': float(row['sog']),
            'lon': float(row['lon']),
            'lat': float(row['lat']),
            'course': float(row['cog']),
            'heading': int(row['heading']),
            'turn': float(row['rot']),
            'status': int(row['nav_status']),
        }
        encoded = encode_dict(input_data)
        decoded = decode(*encoded).asdict()
        return input_data, decoded

    def test_all_rows_produce_valid_nmea(self):
        for _, row in self.sample.iterrows():
            input_data = {
                'type': int(row['msg_type']),
                'mmsi': str(int(row['mmsi'])),
                'speed': float(row['sog']),
                'lon': float(row['lon']),
                'lat': float(row['lat']),
                'course': float(row['cog']),
                'heading': int(row['heading']),
            }
            encoded = encode_dict(input_data)
            assert len(encoded) > 0
            assert encoded[0].startswith("!AIVDM") or encoded[0].startswith("!AIVDO") # !AIVDO is used for AIS messages from own create ship (e.g. for testing)

    def test_all_rows_mmsi_survives_round_trip(self):
        for _, row in self.sample.iterrows():
            input_data, decoded = self._round_trip(row)
            assert str(decoded['mmsi']) == input_data['mmsi']

    def test_all_rows_sog_survives_round_trip(self):
        for _, row in self.sample.iterrows():
            input_data, decoded = self._round_trip(row)
            assert decoded['speed'] == input_data['speed']

    def test_all_rows_cog_survives_round_trip(self):
        for _, row in self.sample.iterrows():
            input_data, decoded = self._round_trip(row)
            assert decoded['course'] == input_data['course']

    def test_all_rows_heading_survives_round_trip(self):
        for _, row in self.sample.iterrows():
            input_data, decoded = self._round_trip(row)
            assert decoded['heading'] == input_data['heading']

    def test_all_rows_lat_survives_round_trip(self):
        for _, row in self.sample.iterrows():
            input_data, decoded = self._round_trip(row)
            assert abs(decoded['lat'] - input_data['lat']) < 0.001

    def test_all_rows_lon_survives_round_trip(self):
        for _, row in self.sample.iterrows():
            input_data, decoded = self._round_trip(row)
            assert abs(decoded['lon'] - input_data['lon']) < 0.001