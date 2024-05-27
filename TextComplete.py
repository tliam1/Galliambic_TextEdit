import difflib
import tkinter as tk
import re
import numpy as np


class TextComplete:
    def __init__(self, tinkerUIWindow, textArea, textCompleteWindow):
        self.textArea = textArea
        self.textCompleteWindow = textCompleteWindow
        self.window = tinkerUIWindow
        self.varNames = ["int", "float", "char", "uint", "uint32", "long", "int32", "string", "void",
                         "bool", "unsigned", "short", "var", "let"]
        self.libraryVars = []
        self.userVars = []
        self.textCompleteWindow.bind("<Button-1>", self.insertSelectedOption)
        self.textCompleteWindow.bind("<Return>", self.insertSelectedOption)
        self.textCompleteWindow.bind("<Shift-Tab>", self.UndoFocus())

    def GatherVariablesAndFunctionNames(self):
        allText = self.textArea.get("1.0", "end-1c")
        # print("TEST")
        varNamesPattern = '|'.join([re.escape(varName) for varName in self.varNames])
        # Match words, including those surrounded by commas or semicolons, excluding varNames
        pattern = fr'''
            \b(?!{varNamesPattern})\b(?![0-9]+\b)\w+\([^()]*\)|\b(?!{varNamesPattern})\b(?![0-9]+\b)\w+\b|(?:"[^"]*"|'[^']*')|,\b(?!{varNamesPattern})\b(?![0-9]+\b)\w+\b,|,\b(?!{varNamesPattern})\b(?![0-9]+\b)\w+\b;|\b(?!{varNamesPattern})\b(?![0-9]+\b)\w+\b;
        '''

        # Find all matches
        matches = re.findall(pattern, allText)
        if matches:
            # remove anything in list that isn't in the current match
            matches = list(set(matches))
            # yields the elements in param1 that are NOT in param2
            difList = np.setdiff1d(self.userVars, matches)
            # print(difList)
            self.userVars = list(filter(lambda i: i not in difList, matches))
            # print(self.userVars)
        else:
            self.userVars.clear()
            print("No variables found")
        pass

    def FilterResults(self):
        word = self.textArea.get("insert-1c wordstart", "insert wordend-1c")
        if len(word) > 0 and len(self.userVars) > 0:
            matches = difflib.get_close_matches(word, self.userVars, len(self.userVars), 0.6)
            if len(matches) >= 1 and word in matches and matches.index(word) != -1:
                matches.remove(word)
            if matches:
                self.showAutoCompleteOptions(matches)
            else:
                self.textCompleteWindow.place_forget()
        else:
            self.textCompleteWindow.place_forget()

            # display matches in visible UI menu

    def showAutoCompleteOptions(self, options):
        self.textCompleteWindow.delete(0, tk.END)
        for option in options:
            self.textCompleteWindow.insert(tk.END, option)
        self.textCompleteWindow.place(relx=0, rely=1.0, anchor="sw")
        self.textCompleteWindow.lift()

    def insertSelectedOption(self, event):
        selected_index = self.textCompleteWindow.curselection()
        if selected_index:
            selected_option = self.textCompleteWindow.get(selected_index)
            self.textArea.delete("insert-1c wordstart", "insert wordend-1c")
            self.textArea.insert("insert", selected_option + " ")
            self.textCompleteWindow.place_forget()
            self.UndoFocus()

    def TakeMainFocus(self):
        self.textCompleteWindow.focus_set()
        self.textCompleteWindow.selection_set(0)

    def UndoFocus(self):
        self.textArea.focus_set()
