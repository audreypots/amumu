#module 1
"""
This module contains the main functions for parsing ISO8583 Packets
based on ISO_Dual_2.19_DraftE document from FD Nashville Canada
"""
def parse_packet(string_value):
    """docstring"""
    ##############################
    # check for NULL value
    ##############################
    string_count = len(string_value)
    print string_count
    if string_count <= 1:
        print "no value"
        return "No Value"

    print "start parsing..."

    ##############################
    # remove white spaces
    ##############################
    input_text_val = string_value.replace(" ", "")
    input_text_val = input_text_val.replace("\n", "")
    input_text_val = input_text_val.replace("\r", "")
    input_text_val = input_text_val.replace("\t", "")
    print "stripping white spaces..."

    # get TPDU
    output_text = "TPDU:\t" + input_text_val[:8] + "\r\n"

    print input_text_val
    print "end parsing..."
    return output_text
