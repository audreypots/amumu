"""
ISO8583 Class Object
"""
import utility

class iso8583(object):
    """
    ISO8583 Packet
        Attributes:
            tpdu: string tpdu value
            bitmap: string bitmap of the packet
            raw_packet: string used in loading the fields
            fields: fields set in the bitmap
            error_msg: error output message
        Methods:
            unpack(string): unpack a valid hex value string and assign the fields
            pack: TODO
            populate_fields: method used to load the fields based on the bitmap
    """
    TPDU_SIZE   = 8
    BMP_SIZE    = 16

    def __init__(self):
        """Return an empty ISO858 object"""
        self.tpdu = ""
        self.bitmap = ""
        self.raw_packet = ""
        self.fields = dict()
        self.error_msg = ""

    def unpack(self, string_value):
        """
        Unpack the packet to each field using bitmap
        returns: valid or invalid
        """
        return_value = "valid"
        string_count = len(string_value)
        if string_count <= 1:
            self.error_msg = "No Value"
            return "invalid"
    
        input_text_val = utility.remove_white_spaces(string_value)
        is_valid = utility.check_valid_hex_val(input_text_val)
        if(is_valid != "valid"):
            self.error_msg = is_valid
            return "invalid"

        # get TPDU
        self.tpdu = input_text_val[:self.TPDU_SIZE]
        input_text_val = input_text_val[self.TPDU_SIZE:]
        # get Bitmap
        self.bitmap = input_text_val[:self.BMP_SIZE]
        input_text_val = input_text_val[self.BMP_SIZE:]
        
        #get fields from bitmap and remaining string
        self.populate_fields(input_text_val)

        return return_value

    def populate_fields(self, string_value):
        #clear fields as we are unpacking a new packet
        self.fields.clear()
        
        #loop through the bitmap
        field = 1
        for x in range(0, 16):
            bit = 8
            for y in range(0, 4):
                if(int(self.bitmap[x], 16) & bit):
                    self.fields[field+y] = ""
                bit /= 2
            field += 4

    def load_field2(self, string_value):
        return_string = ""
        return return_string

    def load_field3(self, string_value):
        return_string = ""
        return return_string

