import tkinter as tk
from tkinter.font import Font

# import tkinter.messagebox
# from tkinter import *
# from tkinter import filedialog
# import ast
from Text_Alignment import TextAlignment
from Menu_Creator import MenuCreator
from File_Saving import FileSaver
from Fonts import TextFonts
from FooterInfoBar import FooterInfoBar

class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Galliambic Editor")
        text_font = Font(family='Times New Roman', size=12)  # weight for boldness and stuff
        self.textArea = tk.Text(self.window, wrap=tk.WORD, font=text_font)
        self.ConfigureTags()
        self.textArea.grid(row=0, column=0, sticky="nsew")

        self.infoBar = tk.Label(self.window, text="Info bar text", bg="lightgray", fg="black", anchor="w")
        self.infoBar.grid(row=1, column=0, sticky="ew")

        self.textFonts = TextFonts(textArea=self.textArea)
        self.textFonts.SetFont('Times New Roman')
        self.textAlign = TextAlignment(tinkerUIWindow=self.window, textArea=self.textArea)
        self.fileSaver = FileSaver(tinkerUIWindow=self.window, textArea=self.textArea)
        self.menuCreator = MenuCreator(tinkerUIWindow=self.window, textArea=self.textArea, fileSaver=self.fileSaver, textAlign=self.textAlign, fonts=self.textFonts)
        self.footerInfoBar = FooterInfoBar(tinkerUIWindow=self.window, infoBar=self.infoBar, mainTextArea=self.textArea)

        self.ConfigureHotKeys()
        self.menuCreator.CreateMenus()
        self.window.mainloop()

    def ConfigureTags(self):
        self.textArea.tag_configure("left", justify="left")
        self.textArea.tag_configure("center", justify="center")
        self.textArea.tag_configure("right", justify="right")

    def ConfigureHotKeys(self):
        self.window.bind_all("<Control-q>", lambda event: self.textAlign.AlignText(-1))
        self.window.bind("<Return>", lambda event: self.textAlign.AlignText(-2))
        self.window.bind("<BackSpace>", lambda event: self.textAlign.AlignText(-3))
        self.window.bind_all("<Key>", lambda event: self.footerInfoBar.UpdateFooter())
        self.window.bind("<Button-1>", lambda event: self.footerInfoBar.UpdateFooter())
