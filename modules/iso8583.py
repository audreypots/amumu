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
            fields: fieds set in the bimap
            error_msg: error output message
        Methods:
            unpack(string): unpack a valid hex value string and assign the fields
            pack: TODO
    """
    TPDU_SIZE   = 8
    BMP_SIZE    = 16

    def __init__(self):
        """Return an empty ISO858 object"""
        self.tpdu = ""
        self.bitmap = "0000000000000000"
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
        return return_value