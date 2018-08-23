"""
Test module for module1.py
"""
import sys
import unittest
from main.modules import module1

class Module1Test(unittest.TestCase):
    """Module1Test"""
    def setUp(self):
        """setUp"""
        pass

    def tearDown(self):
        """tearDown"""
        pass

    #####################
    # remove_white_spaces
    #####################
    def test_remove_white_spaces_tc1(self):
        """remove spaces"""
        self.assertEqual(module1.remove_white_spaces("00 00"),"0000")

    def test_remove_white_spaces_tc2(self):
        """remove \\r"""
        self.assertEqual(module1.remove_white_spaces("00\r00"),"0000")

    def test_remove_white_spaces_tc3(self):
        """remove \\n"""
        self.assertEqual(module1.remove_white_spaces("00\n00"),"0000")

    def test_remove_white_spaces_tc4(self):
        """remove \\t"""
        self.assertEqual(module1.remove_white_spaces("00\t00"),"0000")

    #####################
    # check_valid_hex_val
    #####################
    def test_check_valid_hex_val_tc1(self):
        """return invalid for invalid values"""
        self.assertNotEqual(module1.check_valid_hex_val("G"), "valid")
        self.assertNotEqual(module1.check_valid_hex_val("H"), "valid")
        self.assertNotEqual(module1.check_valid_hex_val("0H"), "valid")

    def test_check_valid_hex_val_tc2(self):
        """
        check for valid hex values
        0-9 and A-F and a-f
        """
        self.assertEqual(module1.check_valid_hex_val("0123456789abcdefABCDEF"), "valid")
        
    #####################
    # parse_packet
    #####################
    def test_parse_packet_tc1(self):
        """NULL input"""
        self.assertEqual(module1.parse_packet(""), "No Value")
