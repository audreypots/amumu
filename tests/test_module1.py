"""
Test module for module1.py
"""
import sys
import unittest
from main.modules import module1

class Module1Test(unittest.TestCase):
    """Module1Test"""
    # preparing to test
    def setUp(self):
        """setUp"""
        pass

    # ending the test
    def tearDown(self):
        """tearDown"""
        pass

    def test_parsepacket_tc1(self):
        """NULL input"""
        self.assertEqual(module1.parse_packet(""), "No Value")
