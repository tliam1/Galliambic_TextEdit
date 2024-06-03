import difflib
import tkinter as tk
import re
import numpy as np
import os

class ShowDirectoryFiles:
    def __init__(self, tinkerUIWindow, textArea, showDirectoryWindow, fileSaver, textHighlighter):
        self.textArea = textArea
        self.directoryWindow = showDirectoryWindow
        self.window = tinkerUIWindow
        self.path = ""
        self.directoryWindow.bind("<Button-1>", self.insertSelectedOption)
        self.fileSaver = fileSaver
        self.textHighlighter = textHighlighter
        self.menuCreator = None
        # self.textCompleteWindow.bind("<Return>", self.insertSelectedOption)
        # self.textCompleteWindow.bind("<Shift-Tab>", self.UndoFocus())

    def showDirectoryOptions(self, files, path):
        self.directoryWindow.delete(0, tk.END)
        self.path = path
        for option in files:
            self.directoryWindow.insert(tk.END, option)
        self.directoryWindow.lift()

    def insertSelectedOption(self, event):
        selected_index = self.directoryWindow.curselection()
        if selected_index:
            self.OpenDirectoryFile(selFile=self.directoryWindow.get(selected_index))
            self.directoryWindow.place_forget()
            self.UndoFocus()

    def TakeMainFocus(self):
        self.directoryWindow.focus_set()
        self.directoryWindow.selection_set(0)

    def UndoFocus(self):
        self.textArea.focus_set()

    def OpenDirectoryFile(self, selFile):
        self.window.title(f"Galliambic Editor: {selFile}")
        # MenuCreator.CreateMenus() do I need this?
        self.textArea.delete(1.0, tk.END)
        # print(self.path)
        fullPath = os.path.join(self.path, selFile)
        # print(fullPath)
        self.fileSaver.SetCurFile(fullPath)
        with open(fullPath, "r") as f:
            content = f.read()
            self.textArea.insert(1.0, content)
        self.menuCreator.CreateMenus()
        self.textHighlighter.FullTextAutoColoring()
