"""
Test module for utility.py
"""
import unittest
from modules import utility

class UtilityTest(unittest.TestCase):
    """UtilityTest"""
    def setUp(self):
        """setUp"""
        pass

    def tearDown(self):
        """tearDown"""
        pass

    #####################
    # remove_white_spaces
    #####################
    def test_util_remove_white_spaces(self):
        """
        remove spaces
        """
        self.assertEqual(utility.remove_white_spaces("00 00"), "0000")
        self.assertEqual(utility.remove_white_spaces("00\r00"), "0000")
        self.assertEqual(utility.remove_white_spaces("00\n00"), "0000")
        self.assertEqual(utility.remove_white_spaces("00\t00"), "0000")

    #####################
    # check_valid_hex_val
    #####################
    def test_util_check_valid_hex_val(self):
        """
        return invalid for invalid values
        """
        self.assertNotEqual(utility.check_valid_hex_val("G"), "valid")
        self.assertNotEqual(utility.check_valid_hex_val("H"), "valid")
        self.assertNotEqual(utility.check_valid_hex_val("0H"), "valid")
        #check for valid hex values
        #0-9 and A-F and a-f
        self.assertEqual(utility.check_valid_hex_val("0123456789abcdefABCDEF"), "valid")
        