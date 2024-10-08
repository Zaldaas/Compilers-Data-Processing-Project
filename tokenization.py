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
        self.kCount, self.iCount, self.lCount, self.oCount, self.sCount, self.cCount = 0, 0, 0, 0, 0, 0
        self.kList, self.iList, self.lList, self.oList, self.sList, self.cList = [], [], [], [], [], []
        # Final output string
        self.excessRemoved = ''
        # Literal/Comment lock, first char comment, valid char reached, repeated space detected
        self.literalLocked, self.commentLocked, self.commentLockedFirstChar, self.charReached, self.removeSpace = False, False, False, False, False
        # Initializing first quote character and first comment character to 'i' to indicate that we are not locked in a literal or comment
        self.firstQuoteChar, self.firstCommentChar = 'i', 'i'
        # Index trackers
        self.prevspaceIndex, self.firstCommentCharIndex, self.nextspaceIndex, self.prevquoteIndex, self.nextquoteIndex, self.nextpunctIndex = 0, 0, 0, 0, 0, 0

    def parse_file(self):
        # Open the file and read the lines
        with open(self.filepath, "r") as file:
            for line in file:
                self.prevspaceIndex = 0
                self.nextspaceIndex = 0
                self.charReached = False
                self.commentLockedFirstChar = False
                self.parse_line(line)
        self.print_results()
    
    def parse_line(self, line):
        for i, char in enumerate(line):
            # Ensure that removeSpace is set to False at the beginning of each character
            self.removeSpace = False
            self.handle_comments(char, i, line)
            self.handle_operators(char)
            self.handle_separators(char)
            self.handle_keywords_identifiers(char, i, line)
            self.handle_literals(char, i, line)
            self.remove_excess(char, i)
    
    def handle_comments(self, char, i, line):
        if self.literalLocked == False and self.commentLocked == False:    
            if char == '#' and self.firstCommentChar == 'i':
                self.commentLocked = True
                # If comment is the first character of the line, we will not output the newline. <- This logic is seen later
                if i == 0:
                    self.commentLockedFirstChar = True
                self.firstCommentChar = char
                self.firstCommentCharIndex = i
                self.cCount += 1
        elif self.literalLocked == False and self.commentLocked == True:
            if char == '\n':
                # Begin resetting the variables for the next line
                tempcString = ''
                for c in line[self.firstCommentCharIndex:i]:
                    tempcString = tempcString + c
                if tempcString not in self.cList:
                    self.cList.append(tempcString)
                self.commentLocked = False
                self.firstCommentChar = 'i'
                self.prevspaceIndex = 0
    
    def handle_operators(self, char):
        if self.literalLocked == False and self.commentLocked == False:     
            if (char in operators):
                self.oCount += 1
                if char not in self.oList:
                    self.oList.append(char)

    def handle_separators(self, char):
        if self.literalLocked == False and self.commentLocked == False:     
            if char in string.punctuation and char != '"' and char != "'" and char not in operators:
                self.sCount += 1
                if char not in self.sList:
                    self.sList.append(char)

    def handle_keywords_identifiers(self, char, i, line):
        if self.literalLocked == False and self.commentLocked == False:     
            # Check if there is a keyword or identifier before the punct for a function call
            koriString = ''
            if not char.isalpha() and not char == '_' and not char.isdigit():
                self.nextpunctIndex = i
                for c in line[self.prevspaceIndex:self.nextpunctIndex]:
                    koriString = koriString + c
                self.prevspaceIndex = self.nextpunctIndex + 1
            elif char == ' ':
                self.nextspaceIndex = i
                for c in line[self.prevspaceIndex:self.nextspaceIndex]:
                    koriString = koriString + c
                self.prevspaceIndex = self.nextspaceIndex + 1
                # Check for repeated spaces and remove them
                if line[i - 1] == ' ':
                    self.removeSpace = True
            if keyword.iskeyword(koriString) or koriString == 'print':
                self.kCount += 1
                if koriString not in self.kList:
                    self.kList.append(koriString)
            elif koriString.isidentifier():
                self.iCount += 1
                if koriString not in self.iList:
                    self.iList.append(koriString)

    def handle_literals(self, char, i, line):
        if self.commentLocked == False:
            # Check for string literal
            if (char == "'" or char == '"'):
                if (char == "'" and line[i + 1] == "'" and line[i + 2] == "'") or (char == '"' and line[i + 1] == '"' and line[i + 2] == '"') or (self.firstQuoteChar == 'i'):
                    # Lock us in a literal, log the first quote character, and increment the literal count
                    self.prevquoteIndex = i
                    self.literalLocked = True
                    self.firstQuoteChar = char
                    self.lCount += 1
                elif (self.firstQuoteChar == char):
                    # Unlock us from the literal and store the string literal
                    if (char == "'" and line[i + 1] == "'" and line[i + 2] == "'") or (char == '"' and line[i + 1] == '"' and line[i + 2] == '"'):
                        self.nextquoteIndex = i + 2
                    else:
                        self.nextquoteIndex = i
                    stringLiteral = ''
                    for c in line[self.prevquoteIndex:self.nextquoteIndex + 1]:
                        stringLiteral = stringLiteral + c
                    if stringLiteral not in self.lList:
                        self.lList.append(stringLiteral)
                    self.literalLocked = False
                    self.firstQuoteChar = 'i'
            # Check if character is a number
            if (char.isdigit()):
                self.lCount += 1
                if char not in self.lList:
                    self.lList.append(char)

    def remove_excess(self, char, i):
        # Check if we have reached a valid character to be printed
        if not self.charReached and (char != ' ' and char != '\n' and char != '#') and not self.commentLockedFirstChar:
            self.charReached = True
        # Add character to final output string
        if self.charReached and not (i == 0 and char == '\n') and not self.removeSpace:
            self.excessRemoved = self.excessRemoved + char

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
        f"{self.kCount + self.iCount + self.lCount + self.oCount + self.sCount + self.cCount}"
        )
        return results
    
    def print_results(self):
        # Print the formatted results of the tokenization
        print(self.format_results())


if __name__ == "__main__":
    parser = CodeParser("test.py")
    parser.parse_file()