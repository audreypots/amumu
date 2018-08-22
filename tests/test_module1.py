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
    # parse_packet
    #####################
    def test_parse_packet_tc1(self):
        """NULL input"""
        self.assertEqual(module1.parse_packet(""), "No Value")
