import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import ast
import os


class MenuCreator:
    def __init__(self, tinkerUIWindow, textArea, fileSaver, textAlign, fonts, directoryWindow):
        self.window = tinkerUIWindow
        self.textArea = textArea
        self.popUpMenu = tk.Menu(self.window, tearoff=0)
        self.fileSaver = fileSaver
        self.textAlign = textAlign
        self.fontList = fonts
        self.directory = directoryWindow

    def CreateMenus(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        self.CreatePopUpMenu()
        self.window.bind("<Button-3>", self.DoPopUp)
        fileMenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New", command=lambda: self.fileSaver.NewFile(MenuCreator=self), state=tk.NORMAL)
        fileMenu.add_command(label="Open", command=lambda: self.fileSaver.OpenFile(MenuCreator=self), state=tk.NORMAL)
        fileMenu.add_command(label="Open Directory", command=lambda: self.GetFilesInDirectory(), state=tk.NORMAL)
        fileMenu.add_command(label="Save", command=self.fileSaver.SaveFile, state=tk.NORMAL if self.fileSaver.currentFile is not None else tk.DISABLED)
        fileMenu.add_command(label="Save As", command=lambda: self.fileSaver.SaveAsFile(MenuCreator=self), state=tk.NORMAL)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.window.quit, state=tk.NORMAL)

        # formatMenu = tk.Menu(menu)
        # menu.add_cascade(label="Format", menu=formatMenu)
        # formatMenu.add_command(label="Cycle With Ctrl+Q", state=tk.DISABLED)
        # formatMenu.add_command(label="Align Text Left", command=lambda: self.textAlign.AlignText(0))
        # formatMenu.add_command(label="Align Text Center", command=lambda: self.textAlign.AlignText(1))
        # formatMenu.add_command(label="Align Text Right", command=lambda: self.textAlign.AlignText(2))
        # formatMenu.add_separator()

        fontMenu = tk.Menu(menu)
        menu.add_cascade(label="Fonts", menu=fontMenu)
        fontMenu.add_command(label="Arial", command=lambda: self.fontList.SetFont("Arial"))
        fontMenu.add_command(label="Times New Roman", command=lambda: self.fontList.SetFont("Times New Roman"))
        fontMenu.add_command(label="Terminal", command=lambda: self.fontList.SetFont("Terminal"))

    def CreatePopUpMenu(self):
        self.popUpMenu = tk.Menu(self.window, tearoff=0)
        # TODO: add something here to actually show the pop up
        self.popUpMenu.add_command(label="Align Text Center", command=lambda: self.textAlign.AlignText(1))
        print("CREATE POP UP")

    def DoPopUp(self, event):
        print(event.x_root)
        try:
            self.popUpMenu.post(event.x_root, event.y_root)
        finally:
            self.popUpMenu.grab_release()
        # print("ATTEMPT POP UP")

    def GetFilesInDirectory(self):
        path = filedialog.askdirectory()
        files = [fn for fn in os.listdir(path) if os.path.isfile(os.path.join(path, fn))]
        # fullPath = []
        # print(files)
        # for filename in files:
        #     fullPath.append(os.path.join(path, filename))

        self.directory.showDirectoryOptions(files=files, path=path)
        pass


