#main file
from Tkinter import Label
from Tkinter import Text
from Tkinter import mainloop
from Tkinter import Tk
from Tkinter import END
from Tkinter import Button
from modules import module1

screen = Tk()

Label(screen, text="Packet (HEX Value ONLY)").grid(row=0, column=0)
Label(screen, text="Output").grid(row=0, column=1)
inputText = Text(screen, height = 50, width = 48)
inputText.grid(row=2,column=0)

outputText = Text(screen, height = 50, width = 48)
outputText.grid(row=2,column=1)

#TODO: test only
inputText.insert(END, "400800091122334455667788")


def parseButtonPress():
    inputTextVal = inputText.get("1.0", END)
    parsedText = module1.parse_packet(inputTextVal)
    outputText.delete("1.0", END)
    outputText.insert(END, parsedText)

parseButton = Button(screen, text = 'Parse Packet', command = parseButtonPress) 
parseButton.grid(row=1, column=0)

mainloop()
