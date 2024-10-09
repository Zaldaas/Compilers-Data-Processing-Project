# Import the required libraries to check for keywords and punctuations
import keyword
import string

# Store a list of python operators
operators = [
    "+", "-", "*", "/", "%", "**", "//",   # Arithmetic Operators
    "=", "+=", "-=", "*=", "/=", "%=", "//=", "**=", "&=", "|=", "^=", ">>=", "<<=",  # Assignment Operators
    "==", "!=", ">", "<", ">=", "<=",   # Comparison Operators
    "&", "|", "^", "~", "<<", ">>"   # Bitwise Operators
]

class CodeParser:
    def __init__(self, filepath):
        self.filepath = filepath
        # Initialize the class with the filepath and counters for tokens
        self.kCount, self.iCount, self.lCount, self.oCount, self.sCount, self.cCount = (
            0, 0, 0, 0, 0, 0
        )
        self.kList, self.iList, self.lList, self.oList, self.sList, self.cList = (
            [], [], [], [], [], []
        )
        # Final output string and docstring string
        self.excessRemoved, self.docstring = '', ''
        # Literal/Comment lock, first char comment, valid char reached, repeated space detected
        self.literalLocked, self.commentLocked, self.docstringLocked = (
            False, False, False
        )
        self.charReached, self.removeSpace = False, False
        # Initializing first quote character and first comment character to 'i' to indicate that we are not locked in a literal or comment
        self.firstQuoteChar, self.firstCommentChar = 'i', 'i'
        # Index trackers and nearby character loggers
        (
            self.prevspaceIndex, self.firstCommentCharIndex, self.firstDocstringCharIndex,
            self.exitingDocstring, self.enteringDocstring, self.nextspaceIndex,
            self.prevquoteIndex, self.nextquoteIndex, self.nextpunctIndex,
            self.doubleOperator
        ) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    def parse_file(self):
        # Open the file and read the lines
        with open(self.filepath, "r") as file:
            for line in file:
                self.reset()
                self.parse_line(line)
        self.print_results()
    
    def parse_line(self, line):
        for i, char in enumerate(line):
            # Ensure that removeSpace is set to False at the beginning of each character
            self.removeSpace = False
            self.handle_comments(char, i, line)
            self.handle_operators(char, i, line)
            self.handle_separators(char)
            self.handle_keywords_identifiers_numbers(char, i, line)
            self.handle_strings_docstrings(char, i, line)
            self.remove_excess(char, i)
    
    def reset(self):
        # Reset the variables for each line
        self.literalLocked, self.commentLocked, self.charReached = (
            False, False, False
        )
        self.firstQuoteChar, self.firstCommentChar = 'i', 'i'
        (
            self.prevspaceIndex, self.firstCommentCharIndex, self.firstDocstringCharIndex, 
            self.nextspaceIndex, self.prevquoteIndex, self.nextquoteIndex, 
            self.nextpunctIndex 
        ) = (0, 0, 0, 0, 0, 0, 0)

    def handle_comments(self, char, i, line):
        # Check if we are still on the tail end of a docstring
        if self.exitingDocstring > 0:
            self.exitingDocstring -= 1
            if self.exitingDocstring == 0:
                self.docstringLocked = False
        if self.enteringDocstring > 0:
            self.enteringDocstring -= 1
        if not self.literalLocked and not self.commentLocked and not self.docstringLocked:
            # Regular # comment handling
            if char == '#' and self.firstCommentChar == 'i':
                self.commentLocked = True
                self.firstCommentChar = char
                self.firstCommentCharIndex = i
                self.cCount += 1
            # Docstring handling
            elif (
                (char == "'" and line[i - 1] == "'" and line[i - 2] == "'") or
                (char == '"' and line[i - 1] == '"' and line[i - 2] == '"')
            ) and self.exitingDocstring == 0:
                self.docstringLocked = True
                self.firstDocstringCharIndex = i - 2
                self.cCount += 1
            # Docstring peak check
            if (
                (char == "'" and line[i + 1] == "'" and line[i + 2] == "'") or
                (char == '"' and line[i + 1] == '"' and line[i + 2] == '"')
            ):
                self.enteringDocstring = 3
        # Regular # comment handling
        elif not self.literalLocked and self.commentLocked and not self.docstringLocked:
            if char == '\n':
                tempcString = ''
                for c in line[self.firstCommentCharIndex:i]:
                    tempcString += c
                if tempcString not in self.cList:
                    self.cList.append(tempcString)
                self.commentLocked = False
        # Docstring handling
        elif not self.literalLocked and not self.commentLocked and self.docstringLocked:
            if char == '\n':
                for c in line[self.firstDocstringCharIndex:i]:
                    self.docstring += c
            elif (
                (char == "'" and line[i + 1] == "'" and line[i + 2] == "'") or
                (char == '"' and line[i + 1] == '"' and line[i + 2] == '"')
            ):
                self.docstring += char + line[i + 1] + line[i + 2]
                if self.docstring not in self.cList:
                    self.cList.append(self.docstring)
                self.exitingDocstring = 3

    def handle_operators(self, char, i, line):
        if self.doubleOperator > 0:
            self.doubleOperator -= 1
        if not self.literalLocked and not self.commentLocked and not self.docstringLocked:
            if char in operators and self.doubleOperator == 0:
                self.oCount += 1
                if char not in self.oList:
                    self.oList.append(char)
                if (line[i + 1] in operators):
                    self.doubleOperator = 2

    def handle_separators(self, char):
        if not self.literalLocked and not self.commentLocked and not self.docstringLocked:
            if (
                char in string.punctuation and char != '"' and char != "'" and
                char != '_' and char not in operators
            ):
                self.sCount += 1
                if char not in self.sList:
                    self.sList.append(char)

    def handle_keywords_identifiers_numbers(self, char, i, line):
        if not self.literalLocked and not self.commentLocked and not self.docstringLocked:
            # Check if there is a keyword or identifier before the punct for a function call
            koriString = ''
            if not char.isalpha() and not char == '_' and not char == ' ' and not char.isdigit():
                self.nextpunctIndex = i
                for c in line[self.prevspaceIndex:self.nextpunctIndex]:
                    koriString += c
                self.prevspaceIndex = self.nextpunctIndex + 1
            elif char == ' ':
                self.nextspaceIndex = i
                for c in line[self.prevspaceIndex:self.nextspaceIndex]:
                    koriString += c
                self.prevspaceIndex = self.nextspaceIndex + 1
                # Check for repeated spaces and remove them
                if line[i - 1] == ' ':
                    self.removeSpace = True
            # Check if the string is a keyword, identifier, or number
            if keyword.iskeyword(koriString) or koriString == 'print':
                self.kCount += 1
                if koriString not in self.kList:
                    self.kList.append(koriString)
            elif koriString.isidentifier():
                self.iCount += 1
                if koriString not in self.iList:
                    self.iList.append(koriString)
            elif koriString.isdigit():
                self.lCount += 1
                if koriString not in self.lList:
                    self.lList.append(koriString)

    def handle_strings_docstrings(self, char, i, line):
        if not self.commentLocked and not self.docstringLocked:
            # Check for string literal and not docstring
            if (
                (char == "'" or char == '"') and not (
                    (
                        (char == "'" and line[i + 1] == "'" and line[i + 2] == "'") or
                        (char == '"' and line[i + 1] == '"' and line[i + 2] == '"')
                    ) or (
                        (char == "'" and line[i - 1] == "'" and line[i + 1] == "'") or
                        (char == '"' and line[i - 1] == '"' and line[i + 1] == '"')
                    ) or (
                        (char == "'" and line[i - 1] == "'" and line[i - 2] == "'") or
                        (char == '"' and line[i - 1] == '"' and line[i - 2] == '"')
                    )
                )
            ):
                if (self.firstQuoteChar == 'i'):
                    # Lock us in a literal, log the first quote character, and increment the literal count
                    self.prevquoteIndex = i
                    self.literalLocked = True
                    self.firstQuoteChar = char
                    self.lCount += 1
                elif (self.firstQuoteChar == char):
                    # Unlock us from the literal and store the string literal
                    self.nextquoteIndex = i
                    stringLiteral = ''
                    for c in line[self.prevquoteIndex:self.nextquoteIndex + 1]:
                        stringLiteral += c
                    if stringLiteral not in self.lList:
                        self.lList.append(stringLiteral)
                    self.literalLocked = False
                    self.firstQuoteChar = 'i'

    def remove_excess(self, char, i):
        # Check if we have reached a valid character to be printed
        # Add character to final output string
        if self.charReached and (
            self.exitingDocstring == 0 and self.enteringDocstring == 0
        ) and not (self.removeSpace or self.commentLocked or self.docstringLocked):
            self.excessRemoved = self.excessRemoved + char
        elif not self.charReached and (
            char != ' ' and char != '\n' and char != '#'
        ) and not (self.commentLocked or self.docstringLocked):
            self.charReached = True
            self.remove_excess(char, i)

    def format_results(self):
        # Format the results
        results = (
        f"{self.excessRemoved}\n"
        "\nCOUNTS\n"
        f"Keywords: {self.kCount}\n"
        f"Identifiers: {self.iCount}\n"
        f"Literals: {self.lCount}\n"
        f"Operators: {self.oCount}\n"
        f"Separators: {self.sCount}\n"
        f"Comments: {self.cCount}\n"
        "\nLISTS\n"
        f"Keywords: {self.kList}\n"
        f"Identifiers: {self.iList}\n"
        f"Literals: {self.lList}\n"
        f"Operators: {self.oList}\n"
        f"Separators: {self.sList}\n"
        f"Comments: {self.cList}\n"
        "\nTOTAL TOKENS\n"
        f"{self.kCount + self.iCount + self.lCount + self.oCount + self.sCount}"
        )
        return results
    
    def print_results(self):
        # Print the formatted results of the tokenization
        print(self.format_results())


if __name__ == "__main__":
    parser = CodeParser("test.py")
    parser.parse_file()