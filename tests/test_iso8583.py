"""
Test module for iso8583.py
"""
import unittest
from modules.iso8583 import Iso8583

class ISO8583Test(unittest.TestCase):
    """ISO8583 Test"""
    def setUp(self):
        """setUp"""
        self.iso = Iso8583()

    def tearDown(self):
        """tearDown"""
        del self.iso

    def test_iso_initialize_val__(self):
        """
        test initial values
        """
        self.assertEqual(self.iso.tpdu, "")
        self.assertEqual(self.iso.msg_type, "")
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
        self.assertEqual(self.iso.TPDU_SIZE, 10)
        self.assertEqual(self.iso.MSG_TYPE_SIZE, 4)
        self.assertEqual(self.iso.BMP_SIZE, 16)
        self.assertEqual(self.iso.PROCESSING_CODE_SIZE, 6)
        self.assertEqual(self.iso.TRANSACTION_AMOUNT_SIZE, 12)

    def test_iso_variable_chk____(self):
        """
        check for parsed values
        that are not fields
        """
        self.iso.unpack("123456789002000000000000000000")
        self.assertEqual(self.iso.tpdu, "1234567890")
        self.assertEqual(self.iso.msg_type, "0200")
        self.assertEqual(self.iso.bitmap, "0000000000000000")

    def test_iso_bitmap_fields___(self):
        """
        test for fields against bitmap
        no value checking yet
        """
        self.iso.unpack(
            "12345678900200F000000000000000161234567890123456123456123456789012"
            )
        self.assertTrue(1 in self.iso.fields)
        self.assertTrue(2 in self.iso.fields)
        self.assertTrue(3 in self.iso.fields)
        self.assertTrue(4 in self.iso.fields)

        self.iso.unpack("123456789004001000000000000002123456789012")
        self.assertTrue(4 in self.iso.fields)
        self.assertTrue(63 in self.iso.fields)

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
        self.assertEquals(popped, "12345")
        self.assertEquals(self.iso.raw_packet, "67890")
        popped = self.iso.pop_value_in_packet(10)
        self.assertEquals(popped, "67890")
        self.assertEquals(self.iso.raw_packet, "")
        #empty raw_packet
        self.iso.raw_packet = ""
        popped = self.iso.pop_value_in_packet(10)
        self.assertEquals(popped, "")
        self.assertEquals(self.iso.raw_packet, "")

    def test_iso_field_02_values_(self):
        """
        test for field 2 (n..19) LLVAR
        """
        #19 digit PAN
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "4000000000000000" #bitmap
        packet += "18123456789012345678" # PAN
        self.iso.unpack(packet)
        self.assertEqual(self.iso.fields[2]['hex_val'], "18123456789012345678")
        self.assertEqual(self.iso.fields[2]['str_val'], "123456789012345678")
        self.assertEqual(self.iso.fields[2]['name'], self.iso.FIELD02_NAME)
        #16 digit PAN
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "4000000000000000" #bitmap
        packet += " 161234567890123456" # PAN
        self.iso.unpack(packet)
        self.assertEqual(self.iso.fields[2]['hex_val'], "161234567890123456")
        self.assertEqual(self.iso.fields[2]['str_val'], "1234567890123456")
        #negative: LL not equal to len(VAR). Field 2 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "4000000000000000" #bitmap
        packet += "19123456789012345678" # PAN
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field02")
        #negative: LL more than 19. Field 2 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "4000000000000000" #bitmap
        packet += "2012345678901234567890" # PAN
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field02")
        #For odd lengths, pad on right with Hex F
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "4000000000000000" #bitmap
        packet += "15371449635398431F" # PAN
        self.iso.unpack(packet)
        self.assertEqual(self.iso.fields[2]['hex_val'], "15371449635398431F")
        self.assertEqual(self.iso.fields[2]['str_val'], "371449635398431")

    def test_iso_field_03_values_(self):
        """
        test for field 3 (n 6) processing code
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "2000000000000000" #bitmap
        packet += "123456" #processing code
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEqual(self.iso.fields[3]['hex_val'], "123456")
        self.assertEqual(self.iso.fields[3]['str_val'], "123456")
        self.assertEqual(self.iso.fields[3]['name'], self.iso.FIELD03_NAME)
        #negative: n not equal to 6. Field 3 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "2000000000000000" #bitmap
        packet += "123" #processing code
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field03")

    def test_iso_field_04_values_(self):
        """
        test for field 4 n 12 transaction amount
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "1000000000000000" #bitmap
        packet += "000000001000" #processing code
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[4]['hex_val'], "000000001000")
        self.assertEquals(self.iso.fields[4]['str_val'], "10.00")
        self.assertEqual(self.iso.fields[4]['name'], self.iso.FIELD04_NAME)
        #negative: n not equal to 12. Field 4 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "1000000000000000" #bitmap
        packet += "000000001" #transaction amount
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field04")

    def test_iso_field_11_values_(self):
        """
        test for field 11 n 6 STAN
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0020000000000000" #bitmap
        packet += "023456" #processing code
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[11]['hex_val'], "023456")
        self.assertEquals(self.iso.fields[11]['str_val'], "23456")
        self.assertEqual(self.iso.fields[11]['name'], self.iso.FIELD11_NAME)
        #negative: n not equal to 6. Field 11 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0020000000000000" #bitmap
        packet += "1234" #stan
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field11")

    def test_iso_field_12_values_(self):
        """
        test for field 12 n 6 transaction local time
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0010000000000000" #bitmap
        packet += "083015" #local time
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[12]['hex_val'], "083015")
        self.assertEquals(self.iso.fields[12]['str_val'], "08:30:15")
        self.assertEqual(self.iso.fields[12]['name'], self.iso.FIELD12_NAME)
        #negative: n not equal to 6. Field 12 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0010000000000000" #bitmap
        packet += "1830" #local time
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field12")

    def test_iso_field_13_values_(self):
        """
        test for field 13 n 4 transaction local date
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0008000000000000" #bitmap
        packet += "0831" #field 13
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[13]['hex_val'], "0831")
        self.assertEquals(self.iso.fields[13]['str_val'], "08/31")
        self.assertEqual(self.iso.fields[13]['name'], self.iso.FIELD13_NAME)
        #negative: n not equal to 4. Field 13 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0008000000000000" #bitmap
        packet += "083" #field 13
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field13")

    def test_iso_field_14_values_(self):
        """
        test for field 14
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0004000000000000" #bitmap
        packet += "0820" #field 14
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[14]['hex_val'], "0820")
        self.assertEquals(self.iso.fields[14]['str_val'], "08/20")
        self.assertEqual(self.iso.fields[14]['name'], self.iso.FIELD14_NAME)
        #negative: n not equal to 4. Field 14 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0004000000000000" #bitmap
        packet += "08" #field 13
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field14")

    def test_iso_field_22_values_(self):
        """
        test for field 22
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000040000000000" #bitmap
        packet += "0051" #field 22
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[22]['hex_val'], "0051")
        self.assertEquals(self.iso.fields[22]['str_val'], "051")
        self.assertEqual(self.iso.fields[22]['name'], self.iso.FIELD22_NAME)
        #negative: n not equal to 4 (3 in specs). Field 22 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000040000000000" #bitmap
        packet += "00" #field 22
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field22")

    def test_iso_field_23_values_(self):
        """
        test for field 23
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000020000000000" #bitmap
        packet += "0001" #field 23
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[23]['hex_val'], "0001")
        self.assertEquals(self.iso.fields[23]['str_val'], "001")
        self.assertEqual(self.iso.fields[23]['name'], self.iso.FIELD23_NAME)
        #negative: n not equal to 4 (3 in specs). Field 23 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000020000000000" #bitmap
        packet += "001" #field 23
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field23")

    def test_iso_field_24_values_(self):
        """
        test for field 24
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000010000000000" #bitmap
        packet += "0048" #field 24
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[24]['hex_val'], "0048")
        self.assertEquals(self.iso.fields[24]['str_val'], "048")
        self.assertEqual(self.iso.fields[24]['name'], self.iso.FIELD24_NAME)
        #negative: n not equal to 3 (3 in specs). Field 24 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000010000000000" #bitmap
        packet += "001" #field 24
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field24")

    def test_iso_field_25_values_(self):
        """
        test for field 25
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000008000000000" #bitmap
        packet += "00" #field 25
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[25]['hex_val'], "00")
        self.assertEquals(self.iso.fields[25]['str_val'], "00")
        self.assertEqual(self.iso.fields[25]['name'], self.iso.FIELD25_NAME)
        #negative: n not equal to 2. Field 25 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000008000000000" #bitmap
        packet += "0" #field 25
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field25")

    def test_iso_field_27_values_(self):
        """
        test for field 27
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000002000000000" #bitmap
        packet += "00" #field 27
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[27]['hex_val'], "00")
        self.assertEquals(self.iso.fields[27]['str_val'], "00")
        self.assertEqual(self.iso.fields[27]['name'], self.iso.FIELD27_NAME)
        #negative: n not equal to 2. Field 27 only
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000002000000000" #bitmap
        packet += "0" #field 27
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field27")

    def test_iso_field_31_values_(self):
        """
        test for field 31
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000000200000000" #bitmap
        packet += "0131" #field 31
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[31]['hex_val'], "0131")
        self.assertEquals(self.iso.fields[31]['str_val'], "1")
        self.assertEqual(self.iso.fields[31]['name'], self.iso.FIELD31_NAME)
        #negative: .. not 4
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000000200000000" #bitmap
        packet += "0" #field 31
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field31")

    def test_iso_field_35_values_(self):
        """
        test for field 35
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000000020000000" #bitmap
        packet += "295435560000000007D120810123456F" #field 35 #TODO
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[35]['hex_val'], "295435560000000007D120810123456F")
        self.assertEquals(self.iso.fields[35]['str_val'], "5435560000000007D120810123456") #TODO
        self.assertEqual(self.iso.fields[35]['name'], self.iso.FIELD35_NAME)
        #negative: not z ..37
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000000020000000" #bitmap
        packet += "295435560000000007D12081012" #field 35
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field35")
        #negative: .. more than 37
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000000020000000" #bitmap
        packet += "385435560000000007D120810121234567890123" #field 35
        self.assertEqual(self.iso.unpack(packet), "invalid")
        self.assertEqual(self.iso.error_msg, "field35")
        

    def test_iso_unpack_input_chk(self):
        """
        test for invalid string values
        """
        self.assertEqual(self.iso.unpack(""), "invalid")
        self.assertEqual(self.iso.error_msg, "No Value")
        self.assertEqual(self.iso.unpack("SS"), "invalid")
        self.assertIsNot(self.iso.error_msg, "valid")
        