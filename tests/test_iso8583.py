"""
Test module for iso8583.py
"""
import sys
import unittest
from modules.iso8583 import iso8583

class ISO8583Test(unittest.TestCase):
    """ISO8583 Test"""
    def setUp(self):
        """setUp"""
        self.iso = iso8583()

    def tearDown(self):
        """tearDown"""
        del self.iso

    def test_iso_initialize_val__(self):
        """
        test initial values
        """
        self.assertEqual(self.iso.tpdu, "")
        self.assertEqual(self.iso.bitmap, "")
        self.assertEqual(self.iso.raw_packet, "")
        self.assertEqual(self.iso.fields, dict())
        self.assertEqual(self.iso.error_msg, "")
        self.assertTrue(2 in self.iso.load_field)
        self.assertTrue(3 in self.iso.load_field)
        self.assertTrue(4 in self.iso.load_field)

    def test_iso_constants_values(self):
        """
        test constant values
        """
        self.assertEqual(self.iso.TPDU_SIZE, 8)
        self.assertEqual(self.iso.BMP_SIZE, 16)

    def test_iso_variable_chk____(self):
        """
        check for parsed values
        that are not fields
        """
        self.iso.unpack("123456780000000000000000")
        self.assertEqual(self.iso.tpdu, "12345678")
        self.assertEqual(self.iso.bitmap, "0000000000000000")

    def test_iso_bitmap_fields___(self):
        """
        test for fields against bitmap
        no value checking yet
        """
        self.iso.unpack("12345678F000000000000000161234567890123456123456")
        self.assertTrue(1 in self.iso.fields)
        self.assertTrue(2 in self.iso.fields)
        self.assertTrue(3 in self.iso.fields)
        self.assertTrue(4 in self.iso.fields)
        
        self.iso.unpack("123456780F00000000000000")
        self.assertTrue(5 in self.iso.fields)
        self.assertTrue(6 in self.iso.fields)
        self.assertTrue(7 in self.iso.fields)
        self.assertTrue(8 in self.iso.fields)

        self.iso.unpack("12345678100000000000000F")
        self.assertTrue(4 in self.iso.fields)
        self.assertTrue(64 in self.iso.fields)
        self.assertTrue(63 in self.iso.fields)
        self.assertTrue(62 in self.iso.fields)
        self.assertTrue(61 in self.iso.fields)

    def test_iso_set_errmsg______(self):
        """
        test set_errmsg
        """
        self.iso.set_errmsg("testerror")
        self.assertEqual(self.iso.error_msg, "testerror")

    def test_iso_is_packet_empty_(self):
        """
        test is_raw_packet_empty
        """
        self.iso.raw_packet = ""
        self.assertTrue(self.iso.is_raw_packet_empty())
        self.iso.raw_packet = "NotEmpty"
        self.assertFalse(self.iso.is_raw_packet_empty())

    def test_iso_pop_value_in_pkt(self):
        """
        test pop_value_in_packet
        """
        self.iso.raw_packet = "1234567890"
        popped = self.iso.pop_value_in_packet(5)
        self.assertEquals(popped,"12345")
        self.assertEquals(self.iso.raw_packet, "67890")
        popped = self.iso.pop_value_in_packet(10)
        self.assertEquals(popped, "67890")
        self.assertEquals(self.iso.raw_packet, "")
        #empty raw_packet
        self.iso.raw_packet =""
        popped = self.iso.pop_value_in_packet(10)
        self.assertEquals(popped, "")
        self.assertEquals(self.iso.raw_packet, "")

    def test_iso_field_2_values__(self):
        """
        test for field 2 (n..19) LLVAR
        """
        #19 digit PAN
        self.iso.unpack("123456784000000000000000191234567890123456789")
        self.assertEqual(self.iso.fields.get(2), "1234567890123456789")
        #16 digit PAN
        self.iso.unpack("123456784000000000000000161234567890123456")
        self.assertEqual(self.iso.fields.get(2), "1234567890123456")
        #negative: LL not equal to len(VAR). Field 2 only
        self.assertEqual(self.iso.unpack(
            "12345678400000000000000019123456789012345678"), "invalid")
        self.assertEqual(self.iso.error_msg, "field2")

    def test_iso_field_3_values__(self):
        """
        test for field 3
        """
        #processing code, n 6
        self.iso.unpack("123456782000000000000000123456")
        self.assertEqual(self.iso.fields.get(3), "123456")
        #negative: n not equal to 6. Field 3 only
        self.assertEqual(self.iso.unpack(
            "123456782000000000000000123"), "invalid")
        self.assertEqual(self.iso.error_msg, "field3")

    def test_iso_unpack_input_chk(self):
        """
        test for invalid string values
        """
        self.assertEqual(self.iso.unpack(""), "invalid")
        self.assertEqual(self.iso.error_msg, "No Value")
        self.assertEqual(self.iso.unpack("SS"), "invalid")
        self.assertIsNot(self.iso.error_msg, "valid")
        
        