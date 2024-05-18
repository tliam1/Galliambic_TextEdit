import tkinter as tk
# import tkinter.messagebox
# from tkinter import *
# from tkinter import filedialog
# import ast
from Text_Alignment import TextAlignment
from Menu_Creator import MenuCreator
from File_Saving import FileSaver

class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Galliambic Editor")
        self.alignText = [["Right", True], ["Center", False], ["Left", False]]
        self.textArea = tk.Text(self.window, wrap=tk.WORD)
        self.ConfigureTags()
        self.textArea.pack(expand=tk.YES, fill=tk.BOTH)
        self.textAlign = TextAlignment(tinkerUIWindow=self.window, textArea=self.textArea)
        self.fileSaver = FileSaver(tinkerUIWindow=self.window, textArea=self.textArea)
        self.menuCreator = MenuCreator(tinkerUIWindow=self.window, textArea=self.textArea, fileSaver=self.fileSaver, textAlign=self.textAlign)
        self.menuCreator.CreateMenus()
        self.window.mainloop()

    def ConfigureTags(self):
        self.textArea.tag_configure("left", justify="left")
        self.textArea.tag_configure("center", justify="center")
        self.textArea.tag_configure("right", justify="right")
