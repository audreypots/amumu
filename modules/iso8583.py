"""
ISO8583 Class Object
"""
import utility

class Iso8583(object):
    """
    ISO8583 Packet
        Attributes:
            tpdu: string tpdu value
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
            set_errmsg: set error_msg
            is_raw_packet_empty: check if raw_packet is empty
                return: True or False
            pop_value_in_packet: pop value in raw_packet
            FIELD METHODS: Loads the Field and returns valid or invalid
            load_field1: for unit test only
            load_field2: PAN
            load_field3: Processing Code
    """
    TPDU_SIZE = 8
    BMP_SIZE = 16
    PROCESSING_CODE_SIZE = 6

    def __init__(self):
        """Return an empty ISO858 object"""
        self.tpdu = ""
        self.bitmap = ""
        self.raw_packet = ""
        self.fields = dict()
        self.load_field = dict({
            1: self.load_field1,
            2: self.load_field2,
            3: self.load_field3,
            4: self.load_field4
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
                    #self.fields[field+y_counter] = ""
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

    def load_field1(self):
        """load field1, unittest purposes"""
        #TODO not really needed
        self.fields[1] = ""
        return "valid"

    def load_field2(self):
        """load field2 n..19 PAN, LLVAR"""
        result_value = "valid"
        err_msg = "field2"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get LL
        size = int(self.pop_value_in_packet(2))
        #get VAR
        pan = self.pop_value_in_packet(size)
        if len(pan) < size:
            self.set_errmsg(err_msg)
            return "invalid"
        self.fields[2] = pan
        return result_value

    def load_field3(self):
        """load field3 n 6 Processing Code"""
        result_value = "valid"
        err_msg = "field3"
        #check first if raw_packet has value
        if self.is_raw_packet_empty():
            self.set_errmsg(err_msg)
            return "invalid"
        #get processing code
        processing_code = self.pop_value_in_packet(self.PROCESSING_CODE_SIZE)
        #check if n 6
        if len(processing_code) != self.PROCESSING_CODE_SIZE:
            self.set_errmsg(err_msg)
            return "invalid"
        self.fields[3] = processing_code
        return result_value

    def load_field4(self):
        """load field 4"""
        pass
