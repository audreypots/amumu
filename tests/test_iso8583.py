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
        check initial values
        """
        self.assertEqual(self.iso.tpdu, "")
        self.assertEqual(self.iso.bitmap, "")
        self.assertEqual(self.iso.fields, dict())
        self.assertEqual(self.iso.error_msg, "")

    def test_iso_constants_values(self):
        """
        check constant values
        """
        self.assertEqual(self.iso.TPDU_SIZE, 8)
        self.assertEqual(self.iso.BMP_SIZE, 16)

    def test_iso_unpack_input_chk(self):
        """
        check for invalid string values
        """
        self.assertEqual(self.iso.unpack(""), "invalid")
        self.assertEqual(self.iso.error_msg, "No Value")
        self.assertEqual(self.iso.unpack("SS"), "invalid")
        self.assertIsNot(self.iso.error_msg, "valid")

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
        check for fields against bitmap
        """
        self.iso.unpack("12345678F000000000000000")
        self.assertEqual(cmp(self.iso.fields,{1:"",2:"",3:"",4:""}), 0)
        
        self.iso.unpack("123456780F00000000000000")
        self.assertEqual(cmp(self.iso.fields,{5:"",6:"",7:"",8:""}), 0)

        self.iso.unpack("12345678FFF0000000000000")
        self.assertEqual(cmp(self.iso.fields,{5:"",6:"",7:"",8:""}), 0)