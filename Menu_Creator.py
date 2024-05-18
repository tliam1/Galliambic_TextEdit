import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import ast


class MenuCreator:
    def __init__(self, tinkerUIWindow, textArea, fileSaver, textAlign):
        self.window = tinkerUIWindow
        self.textArea = textArea
        self.popUpMenu = tk.Menu(self.window, tearoff=0)
        self.fileSaver = fileSaver
        self.textAlign = textAlign

    def CreateMenus(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        self.CreatePopUpMenu()
        self.window.bind("<Button-3>", self.DoPopUp)
        fileMenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New", command=lambda: self.fileSaver.NewFile(MenuCreator=self), state=tk.NORMAL)
        fileMenu.add_command(label="Open", command=lambda: self.fileSaver.OpenFile(MenuCreator=self), state=tk.NORMAL)
        fileMenu.add_command(label="Save", command=self.fileSaver.SaveFile, state=tk.NORMAL if self.fileSaver.currentFile is not None else tk.DISABLED)
        fileMenu.add_command(label="Save As", command=lambda: self.fileSaver.SaveAsFile(MenuCreator=self), state=tk.NORMAL)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.window.quit, state=tk.NORMAL)

        formatMenu = tk.Menu(menu)
        menu.add_cascade(label="Format", menu=formatMenu)
        formatMenu.add_command(label="Cycle With Ctrl+Q", state=tk.DISABLED)
        formatMenu.add_command(label="Align Text Left", command=lambda: self.textAlign.AlignText(0))
        formatMenu.add_command(label="Align Text Center", command=lambda: self.textAlign.AlignText(1))
        formatMenu.add_command(label="Align Text Right", command=lambda: self.textAlign.AlignText(2))

    def CreatePopUpMenu(self):
        self.popUpMenu = tk.Menu(self.window, tearoff=0)
        self.popUpMenu.add_command(label="Align Text Center", command=lambda: self.textAlign.AlignText(1))
        print("CREATE POP UP")

    def DoPopUp(self, event):
        print(event.x_root)
        try:
            self.popUpMenu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popUpMenu.grab_release()
        print("ATTEMPT POP UP")
