from libs.stringTags import formatStringTags

import re

DrawlibStdPalette = {

}

def removeAnsiSequences(inputString):
    # Define a regular expression pattern to match ANSI escape sequences
    ansiPattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    # Use re.sub to replace ANSI sequences with an empty string
    cleanedString = ansiPattern.sub('', inputString)
    return cleanedString

# Function to also autoNone if invalid input is given
def autoNoneColor(color,palette):
    if color == None or palette == None or type(palette) != dict:
        return None
    else:
        if palette.get(color) != None:
            val = palette.get(color)
            if "#" in val:
                background = False
                if val.strip().startswith("#!"):
                    background = True
                    val = val.replace("#!","#",1)
                val = val.replace("#","")
                lv = len(val)
                rgb = [int(val[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)]
                val = '{};2;{};{};{}'.format(48 if background else 38, rgb[0],rgb[1],rgb[2])
            else:
                return val

class TextObj():
    def __init__(self,text,customTags={}):
        self.stdPalette = DrawlibStdPalette
        self.palette = self.stdPalette
        self.text = text
        self.customTags = customTags
    def setPalette(self,palette):
        self.palette = palette
    def resPalette(self):
        self.palette = self.stdPalette
    def setText(self,text):
        self.text = text
    def setTags(self,tags=dict):
        self.customTags = tags
    def retFormat(self):
        # format stringTags
        return formatStringTags(
            inputText=self.text,
            allowedVariables={},
            customTags=self.customTags
        )
    def __str__(self):
        return self.retFormat()
    def __len__(self):
        return len(removeAnsiSequences(self.__str__()))
    def __getitem__(self,index):
        return removeAnsiSequences(self.__str__())[index]
    def split(self,*args,**kwargs):
        return str(self).split(*args,**kwargs)
    def exprt(self) -> dict:
        return {
            "stdPalette": self.stdPalette,
            "palette": self.palette,
            "text": self.text,
            "customTags": self.customTags
        }
    def imprt(self,data=dict):
        self.stdPalette = data["stdPalette"]
        self.palette = data["palette"]
        self.text = data["text"]
        self.customTags = data["customTags"]