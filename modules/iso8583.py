"""
ISO8583 Class Object
"""
import utility

class Iso8583(object):
    """
    ISO8583 Packet
        Attributes:
            tpdu: string tpdu value
            msg_type: string msg_type value
            bitmap: string bitmap of the packet
            raw_packet: string used in loading the fields
            fields: fields set in the bitmap
            error_msg: error output message
        Methods:
            unpack(string): unpack a valid hex value string
                return: valid or invalid
            pack: TODO
            populate_fields: load the fields based on the bitmap
                return: valid or invalid

                {field#:
                    {
                        'name': '',
                        'hex': '',
                        'value': dict or string,
                            if dict
                            {
                                'name': '',
                                'hex': '',
                                'value': dict or string,
                            }

                    }}
            set_errmsg: set error_msg
            is_raw_packet_empty: check if raw_packet is empty
                return: True or False
            pop_value_in_packet: pop value in raw_packet
            display: display unpacked packet
                return: formated fields

            FIELD METHODS: Loads the Field and returns valid or invalid
            load_field01: for unit test only
            load_field02: PAN N..19
            load_field03: Processing Code N 6
            load_field04: Transaction Amount N 12
            load_field11: STAN N 6
            load_field12: Local Transaction Time N 6
            load_field13: Local Transaction Date N 4
            load_field14: Expiration Date N 4
            load_field22: Point of Service Entry Mode N 3 (4)
            load_field23: EMV Card Sequence Number N 3 (4)
            load_field24: Network International Identifier N3 (4)
            load_field25: Point of Service Condition Code N 2
            load_field27: Additional POS information N 2
            load_field31: Acquirer Reference Data AN..1
            load_field35: Track II Data Z..37
            load_field37: Reference Number ANS 12
            load_field38: Approval Code AN 6
            load_field39: Response Code AN 2

            load_field63: Private Use
    """
    #Sizes
    TPDU_SIZE = 10
    MSG_TYPE_SIZE = 4
    BMP_SIZE = 16
    PROCESSING_CODE_SIZE = 6
    TRANSACTION_AMOUNT_SIZE = 12
    STAN_SIZE = 6
    TIME_SIZE = 6
    DATE_SIZE = 4
    EXP_DATE_SIZE = 4
    POSSEM_SIZE = 4 #3
    EMV_CARD_SEQ_SIZE = 4 #3
    NII_SIZE = 4 #3
    POS_CONDITION_CODE_SIZE = 2
    ADD_POS_INFORMATION_SIZE = 2

    #Field names
    FIELD02_NAME = "PAN"
    FIELD03_NAME = "Processing Code"
    FIELD04_NAME = "Transaction Amount"
    FIELD11_NAME = "STAN"
    FIELD12_NAME = "Local Transaction Time"
    FIELD13_NAME = "Local Transaction Date"
    FIELD14_NAME = "Expiry Date"
    FIELD22_NAME = "POSSEM"
    FIELD23_NAME = "EMV Card Seq Number"
    FIELD24_NAME = "NII"
    FIELD25_NAME = "POS Condition Code"
    FIELD27_NAME = "Additional POS Info"
    FIELD31_NAME = "Acq Reference Data"
    FIELD35_NAME = "Track II Data"
    FIELD37_NAME = "Reference Number"
    FIELD38_NAME = "Approval Code"
    FIELD39_NAME = "Response Code"

    def __init__(self):
        """Return an empty ISO858 object"""
        self.tpdu = ""
        self.msg_type = ""
        self.bitmap = ""
        self.raw_packet = ""
        self.fields = dict()
        self.load_field = dict({
            1: self.load_field01,
            2: self.load_field02,
            3: self.load_field03,
            4: self.load_field04,
            11: self.load_field11,
            12: self.load_field12,
            13: self.load_field13,
            14: self.load_field14,
            22: self.load_field22,
            23: self.load_field23,
            24: self.load_field24,
            25: self.load_field25,
            27: self.load_field27,
            31: self.load_field31,
            35: self.load_field35,
            37: self.load_field37,
            38: self.load_field38,
            39: self.load_field39,
            63: self.load_field63
            })
        self.error_msg = ""

    def unpack(self, string_value):
        """
        Unpack the packet to each field using bitmap
        returns: valid or invalid
        """
        return_value = "valid"
        string_count = len(string_value)
        if string_count <= 1:
            self.set_errmsg("No Value")
            return "invalid"
        input_text_val = utility.remove_white_spaces(string_value)
        is_valid = utility.check_valid_hex_val(input_text_val)
        if is_valid != "valid":
            self.set_errmsg(is_valid)
            return "invalid"

        # get TPDU
        self.tpdu = input_text_val[:self.TPDU_SIZE]
        input_text_val = input_text_val[self.TPDU_SIZE:]
        # get Message Type
        self.msg_type = input_text_val[:self.MSG_TYPE_SIZE]
        input_text_val = input_text_val[self.MSG_TYPE_SIZE:]
        # get Bitmap
        self.bitmap = input_text_val[:self.BMP_SIZE]
        input_text_val = input_text_val[self.BMP_SIZE:]

        #get fields from bitmap and remaining string
        if self.populate_fields(input_text_val) != "valid":
            return "invalid"

        return return_value

    def populate_fields(self, string_value):
        """Check the bitmap and load the fields"""
        results_value = "valid"
        #clear fields as we are unpacking a new packet
        self.fields.clear()
        self.raw_packet = string_value
        #loop through the bitmap
        field = 1
        for x_counter in range(0, 16):
            bit = 8
            for y_counter in range(0, 4):
                if int(self.bitmap[x_counter], 16) & bit:
                    if self.load_field[field+y_counter]() != "valid":
                        return "invalid"
                bit /= 2
            field += 4
        return results_value

    def set_errmsg(self, string_value):
        """set error_msg"""
        self.error_msg = string_value

    def is_raw_packet_empty(self):
        """check if raw_packet is empty"""
        if self.raw_packet == "":
            return True
        return False

    def pop_value_in_packet(self, size):
        """
            pop the packet with the given size
        """
        popped = self.raw_packet[:size]
        self.raw_packet = self.raw_packet[size:]
        return popped

    def display(self): #TODO
        """display formatted packet"""
        output_text = "  : " + self.tpdu + "\n  : "
        output_text += self.msg_type + "\n  : "
        output_text += self.bitmap + "\n"
        #for key in self.fields:
        #    field = str(key)
        #    output_text += field.zfill(2) + ": " + self.fields[key] + "\n"
        #for key in self.fields:
        #    if type(key) == dict:
        #        output_text +=
        #        for key2 in key:

        return output_text

    def load_field01(self):
        """load field1, unittest purposes"""
        #TODO not really needed
        self.fields[1] = ""
        return "valid"

    def load_field02(self):
        """load field2 n..19 PAN, LLVAR"""
        result_value = "valid"
        err_msg = "field02"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get LL
        size = int(self.pop_value_in_packet(2))
        hex_size = size
        #check if not more than 19 or equal less than 0
        if size <= 0 or size > 19:
            self.set_errmsg(err_msg)
            return "invalid" 
        #check if odd
        if (size % 2) != 0:
            size += 1
        #get VAR
        pan = self.pop_value_in_packet(size)
        if len(pan) < hex_size:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = str(hex_size) + pan
        str_val = pan[:hex_size]
        self.fields[2] = dict(
            {
                'name': self.FIELD02_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field03(self):
        """load field3 n 6 Processing Code"""
        result_value = "valid"
        err_msg = "field03"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get processing code
        processing_code = self.pop_value_in_packet(
            self.PROCESSING_CODE_SIZE)
        #check if n 6
        if len(processing_code) != self.PROCESSING_CODE_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = processing_code
        str_val = processing_code
        self.fields[3] = dict(
            {
                'name': self.FIELD03_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field04(self):
        """load field 4 n 12 Transaction Amount"""
        result_value = "valid"
        err_msg = "field04"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get transaction amount
        transaction_amount = self.pop_value_in_packet(
            self.TRANSACTION_AMOUNT_SIZE)
        #check if n 12
        if len(transaction_amount) != self.TRANSACTION_AMOUNT_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = transaction_amount
        transaction_amount = str(int(transaction_amount))
        str_val = transaction_amount[:(len(transaction_amount) - 2)]
        str_val += "." + transaction_amount[len(transaction_amount)-2:]
        self.fields[4] = dict(
            {
                'name': self.FIELD04_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field11(self):
        """load field 11 n 6 STAN"""
        result_value = "valid"
        err_msg = "field11"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get STAN
        stan = self.pop_value_in_packet(self.STAN_SIZE)
        #check if n 3
        if len(stan) != self.STAN_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = stan
        str_val = str(int(stan))
        self.fields[11] = dict(
            {
                'name': self.FIELD11_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field12(self):
        """ field 12 n 6 transaction time"""
        result_value = "valid"
        err_msg = "field12"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get Time
        time = self.pop_value_in_packet(self.TIME_SIZE)
        #check if n 6
        if len(time) != self.TIME_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = time
        str_val = time[:2] + ":" + time[2:4] + ":" + time[4:]
        self.fields[12] = dict(
            {
                'name': self.FIELD12_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field13(self):
        """ field 13 n 4 transaction date"""
        result_value = "valid"
        err_msg = "field13"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get date
        date = self.pop_value_in_packet(self.DATE_SIZE)
        #check if n 4
        if len(date) != self.DATE_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = date
        str_val = date[:2] + "/" + date[2:]
        self.fields[13] = dict(
            {
                'name': self.FIELD13_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field14(self):
        """ field 14 n 4 expiry date"""
        result_value = "valid"
        err_msg = "field14"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get exp date
        exp_date = self.pop_value_in_packet(self.EXP_DATE_SIZE)
        #check if n 4
        if len(exp_date) != self.EXP_DATE_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = exp_date
        str_val = exp_date[:2] + "/" + exp_date[2:]
        self.fields[14] = dict(
            {
                'name': self.FIELD14_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field22(self):
        """ field 22 n 4 possem (3 in specs)"""
        result_value = "valid"
        err_msg = "field22"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get possem
        possem = self.pop_value_in_packet(self.POSSEM_SIZE)
        #check if n 4 (3 in specs)
        if len(possem) != self.POSSEM_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = possem
        str_val = possem[1:]
        self.fields[22] = dict(
            {
                'name': self.FIELD22_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field23(self):
        """ field 23 n 3 EMV card sequence number"""
        result_value = "valid"
        err_msg = "field23"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get emv_card_seq
        emv_card_seq = self.pop_value_in_packet(self.EMV_CARD_SEQ_SIZE)
        #check if n 4 (3 in specs)
        if len(emv_card_seq) != self.POSSEM_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = emv_card_seq
        str_val = emv_card_seq[1:]
        self.fields[23] = dict(
            {
                'name': self.FIELD23_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field24(self):
        """load field 24 n 4 (3 in specs)
        network international identifier
        """
        result_value = "valid"
        err_msg = "field24"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get nii
        nii = self.pop_value_in_packet(self.NII_SIZE)
        #check if n 4 (3 in specs)
        if len(nii) != self.NII_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = nii
        str_val = nii[1:]
        self.fields[24] = dict(
            {
                'name': self.FIELD24_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field25(self):
        """load field 25 n 2 point of service condition code"""
        result_value = "valid"
        err_msg = "field25"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get pos condition code
        pos_condition_code = self.pop_value_in_packet(self.POS_CONDITION_CODE_SIZE)
        #check if n 2
        if len(pos_condition_code) != self.POS_CONDITION_CODE_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = pos_condition_code
        str_val = pos_condition_code
        self.fields[25] = dict(
            {
                'name': self.FIELD25_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field27(self):
        """load field 27 n 2 additional pos information"""
        result_value = "valid"
        err_msg = "field27"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get add pos information
        add_pos_information = self.pop_value_in_packet(self.ADD_POS_INFORMATION_SIZE)
        #check if n 2
        if len(add_pos_information) != self.ADD_POS_INFORMATION_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = add_pos_information
        str_val = add_pos_information
        self.fields[27] = dict(
            {
                'name': self.FIELD27_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field31(self):
        """load field 31 an..1 acquirer reference data"""
        result_value = "valid"
        err_msg = "field31"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get add pos information
        acq_ref_data = self.pop_value_in_packet(4)
        #check if n 2
        if len(acq_ref_data) != 4:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = acq_ref_data
        str_val = acq_ref_data[2:].decode("hex")
        self.fields[31] = dict(
            {
                'name': self.FIELD31_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field35(self):
        """load field 35 z..37 track II data"""
        result_value = "valid"
        err_msg = "field35"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get ..
        size = int(self.pop_value_in_packet(2))
        hex_size = size
        #check if not more than 37 or equal less than 0
        if size <= 0 or size > 37:
            self.set_errmsg(err_msg)
            return "invalid" 
        #check if odd
        if (size % 2) != 0:
            size += 1
        #get VAR
        track2 = self.pop_value_in_packet(size)
        if len(track2) < hex_size:
            self.set_errmsg(err_msg)
            return "invalid"
        hex_val = str(hex_size) + track2
        str_val = track2[:hex_size]
        self.fields[35] = dict(
            {
                'name': self.FIELD35_NAME,
                'hex_val': hex_val,
                'str_val': str_val
            }
        )
        return result_value

    def load_field37(self):
        """load field 37 ans 12 reference number"""
        #TODO not really needed
        self.fields[37] = ""
        return "valid"

    def load_field38(self):
        """load field 38 an 6 approval code"""
        #TODO not really needed
        self.fields[38] = ""
        return "valid"

    def load_field39(self):
        """load field 39 an 2 response code"""
        #TODO not really needed
        self.fields[39] = ""
        return "valid"

    def load_field63(self):
        """load field63, unittest purposes"""
        #TODO
        self.fields[63] = ""
        return "valid"
