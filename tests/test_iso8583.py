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
        self.iso.unpack("123456789002004000000000000000191234567890123456789")
        self.assertEqual(self.iso.fields.get(2), "1234567890123456789")
        #16 digit PAN
        self.iso.unpack("123456789004004000000000000000161234567890123456")
        self.assertEqual(self.iso.fields.get(2), "1234567890123456")
        #negative: LL not equal to len(VAR). Field 2 only
        self.assertEqual(self.iso.unpack(
            "12345678900300400000000000000019123456789012345678"), "invalid")
        self.assertEqual(self.iso.error_msg, "field02")

    def test_iso_field_03_values_(self):
        """
        test for field 3 (n 6)
        """
        self.assertEqual(self.iso.unpack(
            "123456789002002000000000000000123456"), "valid")
        self.assertEqual(self.iso.fields.get(3), "123456")
        #negative: n not equal to 6. Field 3 only
        self.assertEqual(self.iso.unpack(
            "123456789002002000000000000000123"), "invalid")
        self.assertEqual(self.iso.error_msg, "field03")

    def test_iso_field_04_values_(self):
        """
        test for field 4
        """
        self.assertEqual(self.iso.unpack(
            "123456789002001000000000000000000000001000"), "valid")
        self.assertEquals(self.iso.fields[4], "000000001000")
        #negative: n not equal to 12. Field 4 only
        self.assertEqual(self.iso.unpack(
            "12345678900200100000000000000000000000100"), "invalid")
        self.assertEqual(self.iso.error_msg, "field04")

    def test_iso_field_11_values_(self):
        """
        test for field 11
        """
        self.assertEqual(self.iso.unpack(
            "123456789002000020000000000000123456"), "valid")
        self.assertEquals(self.iso.fields[11], "123456")
        #negative: n not equal to 6. Field 11 only
        self.assertEqual(self.iso.unpack(
            "1234567890020000200000000000001234"), "invalid")
        self.assertEqual(self.iso.error_msg, "field11")

    def test_iso_field_12_values_(self):
        """
        test for field 12
        """
        self.assertEqual(self.iso.unpack(
            "123456789002000010000000000000654321"), "valid")
        self.assertEquals(self.iso.fields[12], "654321")
        #negative: n not equal to 6. Field 12 only
        self.assertEqual(self.iso.unpack(
            "1234567890020000100000000000001234"), "invalid")
        self.assertEqual(self.iso.error_msg, "field12")

    def test_iso_field_13_values_(self):
        """
        test for field 13
        """
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0008000000000000" #bitmap
        packet += "0831" #field 13
        self.assertEqual(self.iso.unpack(packet), "valid")
        self.assertEquals(self.iso.fields[13], "0831")
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
        self.assertEquals(self.iso.fields[14], "0820")
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
        self.assertEquals(self.iso.fields[22], "0051")
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
        self.assertEquals(self.iso.fields[23], "0001")
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
        self.assertEquals(self.iso.fields[24], "0048")
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
        self.assertEquals(self.iso.fields[25], "00")
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
        self.assertEquals(self.iso.fields[27], "00")
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
        self.assertEquals(self.iso.fields[31], "0131")
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
        self.assertEquals(self.iso.fields[35], "5435560000000007D120810123456F")
        #negative: not z ..37
        packet = "1234567890" #tpdu
        packet += "0200" #msg_type
        packet += "0000000020000000" #bitmap
        packet += "295435560000000007D12081012" #field 35
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
        