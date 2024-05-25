import tkinter as tk
import re


class AutoActions:
    def __init__(self, tinkerUIWindow, textArea):
        self.textArea = textArea
        self.window = tinkerUIWindow
        self.varNames = ["int", "float", "char", "uint", "uint32", "long", "int32", "string", "void",
                         "bool", "unsigned", "short", "var", "let"]
        # self.functionIdentifier = ["()"]

    def AutoIndent(self):
        line = self.textArea.index(f"{tk.INSERT} -1c")  # get current line pos
        textPriorToNewLine = self.textArea.get("1.0", line)
        # Find the position of the last newline character before the current line
        last_newline_index = textPriorToNewLine.rfind('\n')
        if last_newline_index == -1:
            # No previous newline
            start_of_previous_paragraph = "1.0"
        else:
            # New line found
            start_of_previous_paragraph = f"1.0 + {last_newline_index + 1}c"
        # print(self.textArea.get(start_of_previous_paragraph, line))
        tabs = re.findall('\t', self.textArea.get(start_of_previous_paragraph, line))
        # find the most recent paragraph prior to current position
        for tab in tabs:
            self.textArea.insert(tk.INSERT, "\t")

    def AutoColoring(self):
        cursorIndex = self.textArea.index(tk.INSERT)
        lineStartIndex = f"{cursorIndex.split('.')[0]}"
        lineEndIndex = f"{cursorIndex.split('.')[0]}.end"
        allLineText = self.textArea.get(lineStartIndex + ".0", lineEndIndex)
        # Find the last word in the text before the cursor
        matchWord = re.search(r'(\b\w+\b)$', allLineText)
        matchFunction = re.search(r'\b\w+\([^()]*\)', allLineText)
        matchString = re.search(r'([\'"`]).*?\1', allLineText)
        commentPattern = r'(#|\/\/)'
        matchComment = re.search(commentPattern, allLineText)
        if matchWord:
            wordStartIndex = matchWord.start()
            wordEndIndex = matchWord.end()
            wordText = matchWord.group()
            start = f"{lineStartIndex}.{wordStartIndex}"
            end = f"{lineStartIndex}.{wordEndIndex}"
            if wordText in self.varNames:
                self.textArea.tag_add("h_g", start, end)
            else:
                self.textArea.tag_remove("h_g", start, end)

        if matchFunction:
            functionStartIndex = matchFunction.start()
            # wordEndIndex = matchFunction.end()
            wordText = matchFunction.group()
            parenStart = wordText.index("(")
            # for char in wordText:
            start = f"{lineStartIndex}.{functionStartIndex}"
            # end = f"{lineStartIndex}.{wordEndIndex}"
            self.textArea.tag_add("h_b", start, f"{start}+{parenStart}c")
        else:
            # check if there are blue tags on the line, then remove as needed
            self.textArea.tag_remove("h_b", lineStartIndex + ".0", lineEndIndex)

        if matchComment:
            commentStartIndex = matchComment.start()
            commentEndIndex = matchComment.end()
            # wordText = matchComment.group()
            start = f"{lineStartIndex}.{commentStartIndex}"
            end = f"{lineStartIndex}.{commentEndIndex}"
            self.textArea.tag_remove("h_g", start, end)
            self.textArea.tag_remove("h_b", lineStartIndex + ".0", lineEndIndex)
            self.textArea.tag_add("h_p", start, lineEndIndex)
        pass

        if matchString:
            stringStartIndex = matchString.start()
            stringEndIndex = matchString.end()
            # wordText = matchWord.group()
            start = f"{lineStartIndex}.{stringStartIndex}"
            end = f"{lineStartIndex}.{stringEndIndex}"
            self.textArea.tag_add("h_y", start, end)
        else:
            # check if there are blue tags on the line, then remove as needed
            self.textArea.tag_remove("h_y", lineStartIndex + ".0", lineEndIndex)

    def AutoBrackets(self):
        cursor_index = self.textArea.index(tk.INSERT)
        lineStartIndex = f"{int(cursor_index.split('.')[0])-1}"
        self.textArea.insert(tk.INSERT, "\n")
        self.AutoIndent()
        self.textArea.insert(tk.INSERT, "\t")
        self.textArea.insert(tk.INSERT, "\n")
        self.AutoIndent()
        # Go back one space (this should only be tabs at the moment
        self.textArea.delete(f"{tk.INSERT} -1c", tk.INSERT)
        self.textArea.insert(tk.INSERT, "}")
        self.textArea.mark_set("insert", "%d.%d" % (int(lineStartIndex)+2, 0))
        self.AutoIndentPosition()

    def AutoIndentPosition(self):
        # self.textArea.mark_set("insert", tk.END)
        cursorIndex = self.textArea.index(tk.INSERT)
        lineStartIndex = f"{cursorIndex.split('.')[0]}"
        lineEndIndex = f"{cursorIndex.split('.')[0]}.end"
        allLineText = self.textArea.get(lineStartIndex + ".0", lineEndIndex)
        for text in allLineText:
            if text != '\t':
                break
            # move cursor a position over 1 to the right
            self.textArea.mark_set(tk.INSERT, f"{self.textArea.index(tk.INSERT)} +1c")
        pass

    def AutoParen(self):
        self.textArea.insert(tk.INSERT, ")")
        self.textArea.mark_set(tk.INSERT, f"{self.textArea.index(tk.INSERT)} -1c")
        self.AutoColoring()

    def AutoTicks(self, qChar):
        self.textArea.insert(tk.INSERT, f"{qChar}")
        self.textArea.mark_set(tk.INSERT, f"{self.textArea.index(tk.INSERT)} -1c")
        self.AutoColoring()
