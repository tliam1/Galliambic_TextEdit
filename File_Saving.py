import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import ast


class FileSaver:
    def __init__(self, tinkerUIWindow, textArea, TextHighlighter):
        self.window = tinkerUIWindow
        self.textArea = textArea
        self.currentFile = None
        self.textHighlighter = TextHighlighter

    def NewFile(self, MenuCreator):
        res = tkinter.messagebox.askokcancel("Reset File?", "Are you sure you want to reset your file? Any unsaved changes will be discarded.")
        if res:
            # responded with okay
            self.currentFile = None
            MenuCreator.CreateMenus()
            self.textArea.delete(1.0, tk.END)

    def OpenFile(self, MenuCreator):
        file = filedialog.askopenfilename(defaultextension=".txt",
                                          filetypes=[("Text Files", "*.txt"),
                                                     ("C", "*.c"),
                                                     ("C++", "*.cpp"),
                                                     ("JavaScript", "*.js"),
                                                     ("Python", "*.py"),
                                                     ("All Files", "*.*")])
        if file:
            self.window.title(f"Galliambic Editor: {file}")
            self.currentFile = file
            MenuCreator.CreateMenus()
            self.textArea.delete(1.0, tk.END)
            with open(file, "r") as f:
                content = f.read()
                self.textArea.insert(1.0, content)
            self.textHighlighter.FullTextAutoColoring()
        pass

    # def LoadDumpContent(self, dump_content):
    #     tags = {}
    #     for (key, value, index) in dump_content:
    #         if key == "tagon":
    #             if value not in tags:
    #                 tags[value] = [index]
    #             else:
    #                 tags[value].append(index)
    #         elif key == "tagoff":
    #             start_index = tags[value].pop()
    #             self.textArea.tag_add(value, start_index, index)
    #             if not tags[value]:
    #                 del tags[value]
    #         elif key == "mark":
    #             self.textArea.mark_set(value, index)
    #         elif key == "text":
    #             self.textArea.insert(index, value)

    def SaveAsFile(self, MenuCreator):
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt"),
                                                       ("C", "*.c"),
                                                       ("C++", "*.cpp"),
                                                       ("JavaScript", "*.js"),
                                                       ("Python", "*.py"),
                                                       ("All Files", "*.*")])
        if file:
            self.currentFile = file
            MenuCreator.CreateMenus()
            with open(file, "w") as f:
                content = f.read()
                self.textArea.insert(1.0, content)
            self.window.title(f"Galliambic Editor: {file}")
        pass

    def SaveFile(self):
        if self.currentFile:
            with open(self.currentFile, 'w') as f:
                content = self.textArea.dump(1.0, tk.END)
                f.write(str(content))
        pass
