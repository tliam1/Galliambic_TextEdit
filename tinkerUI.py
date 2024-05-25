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
from AutoActions import AutoActions


class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Galliambic Editor")
        text_font = Font(family='Times New Roman', size=12)  # weight for boldness and stuff
        # self.textArea = tk.Text(self.window, wrap=tk.WORD, font=text_font, background="#1E1E1E", foreground="white", insertbackground="lightgrey")

        self.frame = tk.Frame(self.window)
        self.frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.numberBar = tk.Text(self.frame, width=4, padx=5, pady=3, takefocus=0, border=0,
                                 background="lightgray", state="disabled", wrap="none", font=text_font)
        self.numberBar.pack(side="left", fill="y")

        self.textArea = tk.Text(self.frame, wrap=tk.NONE, font=text_font, background="#1E1E1E",
                                foreground="white", insertbackground="lightgrey", undo=True)
        self.textArea.pack(side="left", fill="both", expand=True)

        # self.textArea.grid(row=0, column=1, columnspan=2, sticky="nsew")

        self.infoBar = tk.Label(self.window, text="Info bar text", bg="lightgray", fg="black", anchor="w")
        self.infoBar.grid(row=1, column=0, columnspan=3, sticky="ew")

        # self.numberBar = tk.Label(self.window, text="~", bg="lightgray", fg="black", anchor="w")
        # self.numberBar.grid(row=0, column=0, sticky="ns")

        self.autoActions = AutoActions(tinkerUIWindow=self.window, textArea=self.textArea)
        self.textFonts = TextFonts(textArea=self.textArea)
        self.textFonts.SetFont('Times New Roman')
        self.textAlign = TextAlignment(tinkerUIWindow=self.window, textArea=self.textArea)
        self.fileSaver = FileSaver(tinkerUIWindow=self.window, textArea=self.textArea)
        self.menuCreator = MenuCreator(tinkerUIWindow=self.window, textArea=self.textArea, fileSaver=self.fileSaver, textAlign=self.textAlign, fonts=self.textFonts)
        self.footerInfoBar = FooterInfoBar(tinkerUIWindow=self.window, infoBar=self.infoBar, mainTextArea=self.textArea)

        self.ConfigureTags()
        self.ConfigureHotKeys()
        self.menuCreator.CreateMenus()
        self.window.mainloop()

    def ConfigureTags(self):
        # self.textArea.tag_configure("left", justify="left")
        # self.textArea.tag_configure("center", justify="center")
        # self.textArea.tag_configure("right", justify="right")
        self.textArea.tag_configure("h_g", foreground="lightgreen")
        self.textArea.tag_configure("h_b", foreground="lightblue")
        self.textArea.tag_configure("h_p", foreground="#D3A4FF")
        self.textArea.tag_configure("h_y", foreground="#FFD700")

    def ConfigureHotKeys(self):
        self.window.bind("<BackSpace>", lambda event: self.OnBackSpace())

        self.window.bind("<Key>", lambda event: self.autoActions.AutoColoring())
        self.window.bind("<Shift-{>", lambda event: self.autoActions.AutoBrackets())
        self.window.bind("<Shift-(>", lambda event: self.autoActions.AutoParen())
        self.window.bind("<quoteright>", lambda event: self.autoActions.AutoTicks("'"))
        self.window.bind('<quotedbl>', lambda event: self.autoActions.AutoTicks('"'))
        self.window.bind("`", lambda event: self.autoActions.AutoTicks('`'))
        self.textArea.bind("<Button-1>", lambda event: self.autoActions.AutoIndentPosition())
        self.textArea.bind("<Up>", lambda event: self.autoActions.AutoIndentPosition())
        self.textArea.bind("<Down>", lambda event: self.autoActions.AutoIndentPosition())
        self.window.bind("<Return>", lambda event: self.OnReturn())

        self.textArea.bind("<Key>", lambda event: self.footerInfoBar.UpdateFooter())
        # self.window.bind("<Return>", lambda event: self.footerInfoBar.UpdateFooter())
        self.textArea.bind("<Button-1>", lambda event: self.footerInfoBar.UpdateFooter())
        self.textArea.bind("<BackSpace>", lambda event: self.footerInfoBar.UpdateFooter())
        self.textArea.bind("<Up>", lambda event: self.footerInfoBar.UpdateFooter())
        self.textArea.bind("<Down>", lambda event: self.footerInfoBar.UpdateFooter())

        self.textArea.bind("<KeyRelease>", self.update_number_bar)
        self.textArea.bind("<MouseWheel>", self.update_number_bar)
        self.textArea.bind("<Button-1>", self.update_number_bar)
        self.textArea.bind("<Return>", self.update_number_bar)
        self.textArea.bind("<BackSpace>", self.update_number_bar)

    def update_number_bar(self, event=None):
        self.numberBar.config(state="normal")
        self.numberBar.delete("1.0", "end")

        i = self.textArea.index("@0,0")
        while True:
            dline = self.textArea.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.numberBar.insert("end", linenum + "\n")
            i = self.textArea.index(f"{i}+1line")

        self.numberBar.config(state="disabled")

    def OnReturn(self):
        # Call both AutoIndent and UpdateFooter functions here
        self.autoActions.AutoIndent()
        self.footerInfoBar.UpdateFooter()
        self.textAlign.AlignText(-2)

    def OnBackSpace(self):
        self.textAlign.AlignText(-3)
        self.autoActions.AutoColoring()
