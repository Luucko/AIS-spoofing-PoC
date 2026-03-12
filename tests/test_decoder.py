import pytest
from pyais import decode


class TestBasicDecode:
    """Test that pyais decode correctly parses known NMEA sentences."""

    def test_decodes_type1_message(self):
        msg = "!AIVDM,1,1,,A,13HOI:0P0000VOHLCnHQKwvL05Ip,0*23"
        decoded = decode(msg).asdict()
        assert decoded['msg_type'] == 1
        assert decoded['mmsi'] is not None

    def test_decoded_fields_are_present(self):
        msg = "!AIVDM,1,1,,A,13HOI:0P0000VOHLCnHQKwvL05Ip,0*23"
        decoded = decode(msg).asdict()
        required_fields = ['msg_type', 'mmsi', 'lat', 'lon', 'speed', 'course', 'heading']
        for field in required_fields:
            assert field in decoded, f"Missing field: {field}"

    def test_lat_in_valid_range(self):
        msg = "!AIVDM,1,1,,A,13HOI:0P0000VOHLCnHQKwvL05Ip,0*23"
        decoded = decode(msg).asdict()
        assert -90 <= decoded['lat'] <= 91  # 91 = not available, still valid decode

    def test_lon_in_valid_range(self):
        msg = "!AIVDM,1,1,,A,13HOI:0P0000VOHLCnHQKwvL05Ip,0*23"
        decoded = decode(msg).asdict()
        assert -180 <= decoded['lon'] <= 181  # 181 = not available, still valid decode

    def test_invalid_sentence_raises_error(self):
        with pytest.raises(Exception):
            decode("this is not a valid NMEA sentence")

    def test_bsvdm_prefix_decodes(self):
        """Norwegian feed uses !BSVDM prefix instead of !AIVDM."""
        msg = "!BSVDM,1,1,,B,33oFLL50000RHCFT4la1pGfh0Da:,0*75"
        decoded = decode(msg).asdict()
        assert decoded['msg_type'] == 3
        assert decoded['mmsi'] is not None


class TestDecodeMatchesExpectedValues:
    """Test that a known NMEA sentence decodes to specific expected values."""

    def setup_method(self):
        # This is a real message from our captured data
        self.msg = "!BSVDM,1,1,,B,33oFLL50000RHCFT4la1pGfh0Da:,0*75"
        self.decoded = decode(self.msg).asdict()

    def test_msg_type_is_3(self):
        assert self.decoded['msg_type'] == 3

    def test_mmsi_is_correct(self):
        assert self.decoded['mmsi'] == 259366000

    def test_speed_is_zero(self):
        assert self.decoded['speed'] == 0.0

    def test_lat_is_plausible_norwegian_coast(self):
        assert 55.0 < self.decoded['lat'] < 72.0

    def test_lon_is_plausible_norwegian_coast(self):
        assert 3.0 < self.decoded['lon'] < 32.0