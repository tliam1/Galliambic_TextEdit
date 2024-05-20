import tkinter as tk
import re
import time
# import tkinter.messagebox
# from tkinter import *
# from tkinter import filedialog
# import ast


class FooterInfoBar:
    def __init__(self, tinkerUIWindow, infoBar, mainTextArea):
        self.tinkerUIWindow = tinkerUIWindow
        self.infoBar = infoBar
        self.mainTextArea = mainTextArea
        self.charLen = ""
        self.wordLen = 0
        self.lineLen = 0
        self.curLine = 0
        self.infoBar.config(text=f'Line: {self.curLine}/{self.lineLen}\t\tWords: {self.wordLen}\t\tCharacters: {len(self.charLen)}')

    def UpdateFooter(self):
        # @Todo : expand to show type speed (WPM) by running a process on the sep thread and piping it to this
        self.charLen = self.mainTextArea.get("1.0", "end")
        # wordCount = len(re.findall('\w+', self.charLen))
        self.wordLen = len(re.findall('\w+', self.charLen))
        self.charLen = len(re.findall(r'\S', self.charLen))
        self.lineLen = int(self.mainTextArea.index('end-1c').split('.')[0])
        (line, char) = self.mainTextArea.index(tk.INSERT).split(".")
        self.curLine = int(line)
        self.infoBar.config(text=f'Line: {self.curLine}/{self.lineLen}\t\tWords: {self.wordLen}\t\tCharacters: {self.charLen}')
