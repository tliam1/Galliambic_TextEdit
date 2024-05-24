import tkinter as tk
import re


class AutoActions:
    def __init__(self, tinkerUIWindow, textArea):
        self.textArea = textArea
        self.window = tinkerUIWindow
        self.varNames = ["int", "float", "char", "uint", "uint32", "long", "int32", "string", "void",
                         "bool", "unsigned", "short", "var", "let"]
        self.functionIdentifier = ["()"]

    def AutoIndent(self):
        line = self.textArea.index(f"{tk.INSERT} -1c")  # get current line pos
        textPriorToNewLine = self.textArea.get("1.0", line)
        # Find the position of the last newline character before the current line
        last_newline_index = textPriorToNewLine.rfind('\n')
        print(last_newline_index)
        if last_newline_index == -1:
            # No previous newline
            start_of_previous_paragraph = "1.0"
        else:
            # New line found
            start_of_previous_paragraph = f"1.0 + {last_newline_index + 1}c"
        print(self.textArea.get(start_of_previous_paragraph, line))
        tabs = re.findall('\t', self.textArea.get(start_of_previous_paragraph, line))
        # find the most recent paragraph prior to current position
        for tab in tabs:
            self.textArea.insert(tk.INSERT, "\t")

    def AutoColoring(self):
        cursor_index = self.textArea.index(tk.INSERT)
        line_start_index = f"{cursor_index.split('.')[0]}"
        line_end_index = f"{cursor_index.split('.')[0]}.end"
        text_up_to_cursor = self.textArea.get(line_start_index + ".0", line_end_index)
        # Find the last word in the text before the cursor
        matchWord = re.search(r'(\b\w+\b)$', text_up_to_cursor)
        matchFunction = re.search(r'(\b\w+\([^()]*\))*$', text_up_to_cursor)
        if matchWord:

            word_start_index = matchWord.start()
            word_end_index = matchWord.end()
            word_text = matchWord.group()
            start = f"{line_start_index}.{word_start_index}"
            end = f"{line_start_index}.{word_end_index}"
            if word_text in self.varNames:
                self.textArea.tag_add("h_g", start, end)
            else:
                self.textArea.tag_remove("h_g", start, end)

        if matchFunction:
            word_start_index = matchFunction.start()
            word_end_index = matchFunction.end()
            word_text = matchFunction.group()
            start = f"{line_start_index}.{word_start_index}"
            end = f"{line_start_index}.{word_end_index}"
            if word_text[-2:] in self.functionIdentifier:
                self.textArea.tag_add("h_b", start, f"{end}-2c")
                print(word_text[-2:])
        else:
            # check if there are blue tags on the line, then remove as needed
            pass
        pass
