#main file
from Tkinter import Label
from Tkinter import Text
from Tkinter import mainloop
from Tkinter import Tk
from Tkinter import END
from Tkinter import Button
from modules import iso8583

import sys

screen = Tk()
screen.winfo_toplevel().title("ISO Dual 2.19 Draft E - UNPACKER")

Label(screen, text="Packet (HEX Value ONLY)").grid(row=0, column=0)
Label(screen, text="Output").grid(row=0, column=1)
inputText = Text(screen, height = 50, width = 48)
inputText.grid(row=2,column=0)

outputText = Text(screen, height = 50, width = 48)
outputText.grid(row=2,column=1)

#TODO: test only
inputText.insert(END, "40W800091122334455667788")

def parse_packet(string_value):
    """parse the hex value packet"""
    iso = iso8583.iso8583()
    if(iso.unpack(string_value) != "valid"):
        return iso.error_msg

    

    return "test"

def parseButtonPress():
    inputTextVal = inputText.get("1.0", END)
    parsedText = parse_packet(inputTextVal)
    outputText.delete("1.0", END)
    outputText.insert(END, parsedText)

parseButton = Button(screen, text = 'Parse Packet', command = parseButtonPress) 
parseButton.grid(row=1, column=0)

mainloop()
