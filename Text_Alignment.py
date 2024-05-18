import tkinter as tk
# import tkinter.messagebox
# from tkinter import *
# from tkinter import filedialog
# import ast


class TextAlignment:
    def __init__(self, tinkerUIWindow, textArea):
        self.window = tinkerUIWindow
        self.textArea = textArea
        self.index = 0

    def AlignText(self, index):
        currentLineIndex = self.textArea.index(tk.INSERT)
        # current line index gives a decimal indicating % way through the line
        lineNumber = currentLineIndex.split('.')[0]
        lineStart = f"{lineNumber}.0"
        lineEnd = f"{lineNumber}.{lineNumber}"
        self.textArea.tag_remove("right", lineStart, lineEnd)
        self.textArea.tag_remove("center", lineStart, lineEnd)
        self.textArea.tag_remove("left", lineStart, lineEnd)
        print("index", index)
        print(currentLineIndex.split('.')[1])
        if index == -1:
            self.index += 1
            if self.index > 2:
                self.index = 0
        elif index == -2:
            pass
        elif index == -3:
            if currentLineIndex.split('.')[1] == "0":
                self.index = 0
        else:
            self.index = index

        match self.index:
            case 0:
                self.textArea.tag_add("left", lineStart, lineEnd)
                if self.textArea.get(lineStart, lineEnd) == " ":
                    self.textArea.delete(lineStart)
                pass
            case 1:
                if self.textArea.get(lineStart, lineEnd) == "":
                    self.textArea.insert(lineStart, " ")
                self.textArea.tag_add("center", lineStart, lineEnd)
                pass
            case 2:
                if self.textArea.get(lineStart, lineEnd) == "":
                    self.textArea.insert(lineStart, " ")
                self.textArea.tag_add("right", lineStart, lineEnd)
                pass

        pass
