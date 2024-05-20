import tkinter as tk
from tkinter import font


class TextFonts:
    def __init__(self, textArea):
        self.fonts = list(font.families())
        self.fonts.sort()
        self.textArea = textArea

    def SetFont(self, fontName):
        tagName = f"font_{fontName}"
        self.textArea.tag_configure(tagName, font=(fontName, 12))
        self.textArea.bind("<KeyPress>", lambda event: self.ApplyFontToNewText(event, tagName), add="+")

    def RemoveExistingFont(self, startIndex, endIndex):
        tagsAtIndex = self.textArea.tag_names(startIndex)
        for tag in tagsAtIndex:
            if tag.startswith("font_"):
                # Remove the tag if it starts with "font_"
                self.textArea.tag_remove(tag, startIndex, endIndex)

    def ApplyFontToNewText(self, event, tagName):
        if event.char.isalpha():
            # @Todo : currently if we swap fonts between two letters it swaps the prior letter too, otherwise all good
            currentIndex = self.textArea.index(tk.INSERT)
            previousIndex = self.textArea.index(tk.INSERT + "-1c")
            self.RemoveExistingFont(previousIndex, currentIndex + " wordend")
            self.textArea.tag_add(tagName, previousIndex, currentIndex + " wordend")



