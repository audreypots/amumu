"""
Utility Module
"""



def check_valid_hex_val(string_value):
    """
    check for valid hex values
    0-9 and A-F and a-f
    """
    return_value = "valid"
    letter_index = 0
    for letter_in_string_value in string_value:
        letter_index += 1
        if(letter_in_string_value >= "0" and letter_in_string_value <= "9"):
            continue
        elif(letter_in_string_value >= "A" and letter_in_string_value <= "F"):
            continue
        elif(letter_in_string_value >= "a" and letter_in_string_value <= "f"):
            continue
        else:
            return_value = "Invalid Hex Value[" + letter_in_string_value + "] at location[" + str(letter_index) + "]"
            break
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