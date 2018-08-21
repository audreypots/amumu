#module 1

def parsePacket(s):
    ##############################
    # check for NULL value
    ##############################
    sCount = len(s)
    print(sCount)
    if sCount <= 1:
        print("no value")
        return "No Value"

    print("start parsing...")

    ##############################
    # remove white spaces
    ##############################
    inputTextVal = s.replace(" ","")
    inputTextVal = inputTextVal.replace("\n","")
    inputTextVal = inputTextVal.replace("\r","")
    inputTextVal = inputTextVal.replace("\t","")
    print("stripping white spaces...")

    # get TPDU
    outputText = "TPDU:\t" + inputTextVal[:8] + "\r\n"

    print(inputTextVal)
    print("end parsing...")
    return outputText
