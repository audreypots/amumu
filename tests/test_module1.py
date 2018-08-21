import sys
import unittest

sys.path.append("/Users/mauricegonzales/Documents/PYTHON/iso_dual_2.19_parser")
from main import module1

class module1Test(unittest.TestCase):
	# preparing to test
	def setUp(self):
		pass

	# ending the test
	def tearDown(self):
		pass

	def test_parsePacket_tc1(self):
		self.assertEqual( module1.parsePacket("AAA"), "")