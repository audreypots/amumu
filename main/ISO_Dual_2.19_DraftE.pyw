#main file
from Tkinter import *
from module1 import parsePacket

screen = Tk()

Label(screen, text="Packet (HEX Value ONLY)").grid(row=0, column=0)
Label(screen, text="Output").grid(row=0, column=1)
inputText = Text(screen, height = 50, width = 48)
inputText.grid(row=1,column=0)

outputText = Text(screen, height = 50, width = 48)
outputText.grid(row=1,column=1)

def parseButtonPress():
    inputTextVal = inputText.get("1.0", END)
    parsedText = parsePacket(inputTextVal)
    outputText.delete("1.0", END)
    outputText.insert(END, parsedText)
    
parseButton = Button(screen, text = 'Parse Packet', command = parseButtonPress) 
parseButton.grid(row=2, column=0)
 
mainloop()
