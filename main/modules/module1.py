#module 1
"""
This module contains the main functions for parsing ISO8583 Packets
based on ISO_Dual_2.19_DraftE document from FD Nashville Canada
"""
def parse_packet(string_value):
    """parse the hex value packet"""
    ##############################
    # check for NULL value
    ##############################
    string_count = len(string_value)
    if string_count <= 1:
        return "No Value"

    input_text_val = remove_white_spaces(string_value)

    if(check_valid_hex_val(input_text_val) == "invalid"):
        return "Invalid Hex Values"

    # get TPDU
    output_text = "TPDU:\t" + input_text_val[:8] + "\r\n"

    return output_text

def check_valid_hex_val(string_value):
    """
    check for valid hex values
    0-9 and A-F and a-f
    """
    return_value = "valid"
    for letter_in_string_value in string_value:
        if(letter_in_string_value >= "0" and letter_in_string_value <= "9"):
            continue
        elif(letter_in_string_value >= "A" and letter_in_string_value <= "F"):
            continue
        elif(letter_in_string_value >= "a" and letter_in_string_value <= "f"):
            continue
        else:
            return_value = "invalid"
    return return_value

def remove_white_spaces(string_value):
    """remove white spaces"""
    ##############################
    # remove white spaces
    ##############################
    input_text_val = string_value.replace(" ", "")
    input_text_val = input_text_val.replace("\n", "")
    input_text_val = input_text_val.replace("\r", "")
    input_text_val = input_text_val.replace("\t", "")
    return input_text_val