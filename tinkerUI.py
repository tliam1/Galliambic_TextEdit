import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import ast

class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Galliambic Editor")
        self.alignText = [["Right", True], ["Center", False], ["Left", False]]
        self.textArea = tk.Text(self.window, wrap=tk.WORD)
        self.textArea.tag_configure("left", justify="left")
        self.textArea.tag_configure("center", justify="center")
        self.textArea.tag_configure("right", justify="right")
        self.currentFile = None
        self.textArea.pack(expand=tk.YES, fill=tk.BOTH)
        self.CreateMenus()
        self.window.mainloop()

    def CreateMenus(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)

        fileMenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New", command=self.NewFile, state=tk.NORMAL)
        fileMenu.add_command(label="Open", command=self.OpenFile, state=tk.NORMAL)
        fileMenu.add_command(label="Save", command=self.SaveFile, state=tk.NORMAL if self.currentFile is not None else tk.DISABLED)
        fileMenu.add_command(label="Save As", command=self.SaveAsFile, state=tk.NORMAL)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.window.quit, state=tk.NORMAL)

        formatMenu = tk.Menu(menu)
        menu.add_cascade(label="Format", menu=formatMenu)
        formatMenu.add_checkbutton(label="Align Text Left", command=lambda: self.AlignText(0))
        formatMenu.add_checkbutton(label="Align Text Center", command=lambda: self.AlignText(1))
        formatMenu.add_checkbutton(label="Align Text Right", command=lambda: self.AlignText(2))

    def NewFile(self):
        res = tkinter.messagebox.askokcancel("Reset File?", "Are you sure you want to reset your file? Any unsaved changes will be discarded.")
        if res:
            # responded with okay
            self.currentFile = None
            self.CreateMenus()
            self.textArea.delete(1.0, tk.END)

    def OpenFile(self):
        file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            self.window.title(f"Galliambic Editor: {file}")
            self.currentFile = file
            self.CreateMenus()
            self.textArea.delete(1.0, tk.END)
            with open(file, "r") as f:
                content = f.read()
                dump_content = ast.literal_eval(content)
                print(dump_content)
                self.LoadDumpContent(dump_content)

        pass

    def LoadDumpContent(self, dump_content):
        tags = {}
        for (key, value, index) in dump_content:
            if key == "tagon":
                if value not in tags:
                    tags[value] = [index]
                else:
                    tags[value].append(index)
            elif key == "tagoff":
                start_index = tags[value].pop()
                self.textArea.tag_add(value, start_index, index)
                if not tags[value]:
                    del tags[value]
            elif key == "mark":
                self.textArea.mark_set(value, index)
            elif key == "text":
                self.textArea.insert(index, value)

    def SaveAsFile(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            self.currentFile = file
            self.CreateMenus()
            with open(file, "w") as f:
                content = self.textArea.dump(1.0, tk.END)
                f.write(str(content))
            self.window.title(f"Galliambic Editor: {file}")
        pass

    def SaveFile(self):
        if self.currentFile:
            with open(self.currentFile, 'w') as f:
                content = self.textArea.dump(1.0, tk.END)
                f.write(str(content))
        pass

    def AlignText(self, index):
        currentLineIndex = self.textArea.index(tk.INSERT)
        print(currentLineIndex)
        # current line index gives a decimal indicating % way through the line
        lineNumber = currentLineIndex.split('.')[0]
        print(lineNumber)
        lineStart = f"{lineNumber}.0"
        lineEnd = f"{lineNumber}.{lineNumber}"
        print(lineStart)
        print(lineEnd)
        self.textArea.tag_remove("right", lineStart, lineEnd)
        self.textArea.tag_remove("center", lineStart, lineEnd)
        self.textArea.tag_remove("left", lineStart, lineEnd)
        match index:
            case 0:
                self.textArea.tag_add("left", lineStart, lineEnd)
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
