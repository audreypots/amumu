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

    def test_class_init_tc1(self):
        """
        check initial values
        """
        self.assertEqual(self.iso.tpdu, "")
        self.assertEqual(self.iso.bitmap, "0000000000000000")
        self.assertEqual(self.iso.fields, dict())
        self.assertEqual(self.iso.error_msg, "")

    def test_class_constants_tc2(self):
        """
        check initial values
        """
        self.assertEqual(self.iso.TPDU_SIZE, 8)
        self.assertEqual(self.iso.BMP_SIZE, 16)