"""
Test module for module1.py
"""
import sys
import unittest

#TODO: working in Windows even if the path is wrong in sys.path.append,
# module was still imported if discover is used and not running the test module.py
sys.path.append("/Users/mauricegonzales/Documents/PYTHON/iso_dual_2.19_parser")

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
