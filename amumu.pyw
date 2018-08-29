"""
Main File: Start here
"""
from Tkinter import Label
from Tkinter import Text
from Tkinter import mainloop
from Tkinter import Tk
from Tkinter import END
from Tkinter import Button
from modules import iso8583

SCREEN = Tk()
SCREEN.winfo_toplevel().title("ISO Dual 2.19 Draft E - UNPACKER")

Label(SCREEN, text="Packet (HEX Value ONLY)").grid(row=0, column=0)
Label(SCREEN, text="Output").grid(row=0, column=1)
INPUTTEXT = Text(SCREEN, height=50, width=48)
INPUTTEXT.grid(row=2, column=0)

OUTPUTTEXT = Text(SCREEN, height=50, width=48)
OUTPUTTEXT.grid(row=2, column=1)

#TODO: test only
INPUTTEXT.insert(END, "40W800091122334455667788")

def parse_packet(string_value):
    """parse the hex value packet"""
    iso = iso8583.iso8583()
    if iso.unpack(string_value) != "valid":
        return iso.error_msg
    return "test"

def parse_button_press():
    """when button is pressed"""
    input_text_val = INPUTTEXT.get("1.0", END)
    parsed_text = parse_packet(input_text_val)
    OUTPUTTEXT.delete("1.0", END)
    OUTPUTTEXT.insert(END, parsed_text)

PARSE_BUTTON = Button(SCREEN, text='Parse Packet', command=parse_button_press)
PARSE_BUTTON.grid(row=1, column=0)

mainloop()
