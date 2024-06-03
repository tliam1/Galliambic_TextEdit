import tkinter as tk
import re


class AutoActions:
    def __init__(self, tinkerUIWindow, textArea):
        self.textArea = textArea
        self.window = tinkerUIWindow
        self.varNames = ["int", "float", "char", "uint", "uint32", "long", "int32", "string", "void",
                         "bool", "unsigned", "short", "var", "let", "struct", "return", "enum", "union"]
        self.blockCommentBeginLine = '1.0'
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
        # print(len(tabs))
        # find the most recent paragraph prior to current position
        for tab in tabs:
            self.textArea.insert(tk.INSERT, "\t")

    def AutoColoring(self):
        cursorIndex = self.textArea.index(tk.INSERT)
        lineStartIndex = f"{cursorIndex.split('.')[0]}.0"
        lineEndIndex = f"{cursorIndex.split('.')[0]}.end"
        allLineText = self.textArea.get(lineStartIndex, lineEndIndex)

        # Clear previous tags on the line
        self.textArea.tag_remove("h_g", lineStartIndex, lineEndIndex)
        self.textArea.tag_remove("h_b", lineStartIndex, lineEndIndex)
        self.textArea.tag_remove("h_p", lineStartIndex, lineEndIndex)
        self.textArea.tag_remove("h_y", lineStartIndex, lineEndIndex)

        # Apply comment highlighting first
        matchComment = re.search(r'(#|//).*', allLineText)
        if matchComment:
            commentStartIndex = matchComment.start()
            start = f"{lineStartIndex}+{commentStartIndex}c"
            self.textArea.tag_add("h_p", start, lineEndIndex)
            return  # No further processing needed for this line

        # Detect multi-line block comments
        blockCommentStart = re.search(r'/\*', allLineText)
        if blockCommentStart:
            self.blockCommentBeginLine = cursorIndex.split('.')[0] + ".0"
            startLineNum = cursorIndex.split('.')[0]
            start = f"{startLineNum}.0+{blockCommentStart.start()}c"
            end = lineEndIndex
            self.textArea.tag_add("h_p", start, end)
            return

        # Check if currently inside a multi-line block comment
        previousLinesText = self.textArea.get(self.blockCommentBeginLine, lineStartIndex)
        if re.search(r'/\*', previousLinesText) and not re.search(r'\*/', previousLinesText):
            self.textArea.tag_add("h_p", lineStartIndex, lineEndIndex)
            return

        # Apply string highlighting
        matchString = re.finditer(r'([\'"`]).*?\1', allLineText)
        for match in matchString:
            stringStartIndex = match.start()
            stringEndIndex = match.end()
            start = f"{lineStartIndex}+{stringStartIndex}c"
            end = f"{lineStartIndex}+{stringEndIndex}c"
            self.textArea.tag_add("h_y", start, end)

        # Apply function highlighting
        matchFunction = re.finditer(r'\b(?![0-9]+\b)\w+\(|\b(?![0-9]+\b)\w+\s+\(', allLineText)
        for match in matchFunction:
            functionStartIndex = match.start()
            parenStart = match.group().index("(")
            start = f"{lineStartIndex}+{functionStartIndex}c"
            self.textArea.tag_add("h_b", start, f"{start}+{parenStart}c")

        # Apply variable name highlighting
        matchWords = re.finditer(r'\b\w+\b', allLineText)
        for match in matchWords:
            wordText = match.group()
            if wordText in self.varNames:
                wordStartIndex = match.start()
                wordEndIndex = match.end()
                start = f"{lineStartIndex}+{wordStartIndex}c"
                end = f"{lineStartIndex}+{wordEndIndex}c"
                self.textArea.tag_add("h_g", start, end)

        # Apply number highlighting
        matchNumbers = re.finditer(r'[0-9]+', allLineText)
        for matchNumber in matchNumbers:
            numberStartIndex = matchNumber.start()
            numberEndIndex = matchNumber.end()
            start = f"{lineStartIndex}+{numberStartIndex}c"
            end = f"{lineStartIndex}+{numberEndIndex}c"
            self.textArea.tag_add("h_r", start, end)

    def AutoBrackets(self):
        cursor_index = self.textArea.index(tk.INSERT)
        lineStartIndex = f"{int(cursor_index.split('.')[0]) - 1}"
        self.textArea.insert(tk.INSERT, "\n")
        self.AutoIndent()
        self.textArea.insert(tk.INSERT, "\t")
        self.textArea.insert(tk.INSERT, "\n")
        self.AutoIndent()
        # Go back one space (this should only be tabs at the moment
        self.textArea.delete(f"{tk.INSERT} -1c", tk.INSERT)
        self.textArea.insert(tk.INSERT, "}")
        self.textArea.mark_set("insert", "%d.%d" % (int(lineStartIndex) + 2, 0))
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

    def FullTextAutoColoring(self):
        allText = self.textArea.get("1.0", "end-1c")

        # Clear all previous tags
        self.textArea.tag_remove("h_g", "1.0", "end")
        self.textArea.tag_remove("h_b", "1.0", "end")
        self.textArea.tag_remove("h_p", "1.0", "end")
        self.textArea.tag_remove("h_y", "1.0", "end")

        lines = allText.split("\n")

        for line_num, line in enumerate(lines, start=1):
            lineStartIndex = f"{line_num}.0"
            lineEndIndex = f"{line_num}.end"

            # Apply comment highlighting first
            matchComments = re.finditer(r'(#|//).*', line)
            for match in matchComments:
                commentStartIndex = match.start()
                start = f"{lineStartIndex}+{commentStartIndex}c"
                self.textArea.tag_add("h_p", start, lineEndIndex)
                continue  # Skip further processing for this line

            # Detect multi-line block comments
            blockCommentStart = re.search(r'/\*', line)
            if blockCommentStart:
                self.blockCommentBeginLine = lineStartIndex
                start = f"{lineStartIndex}+{blockCommentStart.start()}c"
                self.textArea.tag_add("h_p", start, lineEndIndex)
                continue

            # Check if currently inside a multi-line block comment
            previousLinesText = self.textArea.get(self.blockCommentBeginLine, lineStartIndex)
            if re.search(r'/\*', previousLinesText) and not re.search(r'\*/', previousLinesText):
                self.textArea.tag_add("h_p", lineStartIndex, lineEndIndex)
                continue


            # Apply string highlighting
            matchStrings = re.finditer(r'([\'"`]).*?\1', line)
            for match in matchStrings:
                stringStartIndex = match.start()
                stringEndIndex = match.end()
                start = f"{lineStartIndex}+{stringStartIndex}c"
                end = f"{lineStartIndex}+{stringEndIndex}c"
                self.textArea.tag_add("h_y", start, end)

            # Apply function highlighting
            matchFunctions = re.finditer(r'\b(?![0-9]+\b)\w+\(|\b(?![0-9]+\b)\w+\s+\(', line)
            for match in matchFunctions:
                functionStartIndex = match.start()
                parenStart = match.group().index("(")
                start = f"{lineStartIndex}+{functionStartIndex}c"
                self.textArea.tag_add("h_b", start, f"{start}+{parenStart}c")

            # Apply variable name highlighting
            matchWords = re.finditer(r'\b\w+\b', line)
            for match in matchWords:
                wordText = match.group()
                if wordText in self.varNames:
                    wordStartIndex = match.start()
                    wordEndIndex = match.end()
                    start = f"{lineStartIndex}+{wordStartIndex}c"
                    end = f"{lineStartIndex}+{wordEndIndex}c"
                    self.textArea.tag_add("h_g", start, end)

            # Apply number highlighting
            matchNumbers = re.finditer(r'[0-9]+', line)
            for matchNumber in matchNumbers:
                numberStartIndex = matchNumber.start()
                numberEndIndex = matchNumber.end()
                start = f"{lineStartIndex}+{numberStartIndex}c"
                end = f"{lineStartIndex}+{numberEndIndex}c"
                self.textArea.tag_add("h_r", start, end)