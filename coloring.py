from distutils.sysconfig import customize_compiler
from typing import Text
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