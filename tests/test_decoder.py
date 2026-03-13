import pytest
from pyais import decode


class TestBasicDecode:
    """Test that pyais decode correctly parses known NMEA sentences."""

    def setup_method(self):
        """Define test input used across basic encode tests."""
        self.msg = "!AIVDM,1,1,,A,13HOI:0P0000VOHLCnHQKwvL05Ip,0*23"    # Example AIS message from pyais library: https://github.com/M0r13n/pyais/blob/master/examples/decode.py
        self.decoded = decode(self.msg).asdict()

    def test_decodes_type1_message(self):
        assert self.decoded['msg_type'] == 1
        assert self.decoded['mmsi'] is not None

    def test_decoded_fields_are_present(self):
        required_fields = ['msg_type', 'mmsi', 'lat', 'lon', 'speed', 'course', 'heading']
        for field in required_fields:
            assert field in self.decoded, f"Missing field: {field}"

    def test_lat_in_valid_range(self):
        assert -90 <= self.decoded['lat'] <= 91         # 91 = not available, still valid decode

    def test_lon_in_valid_range(self):
        assert -180 <= self.decoded['lon'] <= 181       # 181 = not available, still valid decode

    def test_invalid_sentence_raises_error(self):
        with pytest.raises(Exception):
            decode("this is not a valid NMEA sentence")

    def test_bsvdm_prefix_decodes(self):
        """Norwegian feed uses !BSVDM prefix instead of !AIVDM."""
        msg = "!BSVDM,1,1,,B,33oFLL50000RHCFT4la1pGfh0Da:,0*75"     # First AIS message from data\processed\ais_decoded_20260305_2124.csv
        decoded = decode(msg).asdict()
        assert decoded['msg_type'] == 3
        assert decoded['mmsi'] is not None


class TestDecodeMatchesExpectedValues:
    """Test that a known NMEA sentence decodes to specific expected values."""

    def setup_method(self):
        self.msg = "!BSVDM,1,1,,B,33oFLL50000RHCFT4la1pGfh0Da:,0*75"
        self.decoded = decode(self.msg).asdict()

    def test_msg_type_is_3(self):
        assert self.decoded['msg_type'] == 3        # Payload starts with 3 => message type 3, also confirmed through third-party AIS decoder: https://www.aggsoft.com/ais-decoder.htm

    def test_mmsi_is_correct(self):
        assert self.decoded['mmsi'] == 259366000    # Gathered through third-party AIS decoder: https://www.aggsoft.com/ais-decoder.htm

    def test_speed_is_zero(self):
        assert self.decoded['speed'] == 0.0         # Gathered through third-party AIS decoder: https://www.aggsoft.com/ais-decoder.htm 

    def test_lat_is_plausible_norwegian_coast(self):
        assert 55.0 < self.decoded['lat'] < 72.0    # Norway's approximately latitude range

    def test_lon_is_plausible_norwegian_coast(self):
        assert 3.0 < self.decoded['lon'] < 32.0     # Norway's approximately longitude range

    def test_status(self):
        assert self.decoded['status'] == 5          # Gathered through third-party AIS decoder: https://www.aggsoft.com/ais-decoder.htm