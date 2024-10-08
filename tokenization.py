# Import the required libraries to check for keywords and punctuations
import keyword
import string

# Initialize the variables to count the number of keywords, identifiers, literals, operators, separators, and comments
kCount = 0
kList = []
iCount = 0
iList = []
lCount = 0
lList = []
oCount = 0
oList = []
sCount = 0
sList = []
cCount = 0
cList = []
# String to check if keyword or identifier
koriString = ''
# String to store string literals
stringLiteral = ''
# Initialize the variables to check if we are locked in a literal or comment
literalLocked = False
commentLocked = False
# Initializing first quote character and first comment character to 'i' to indicate that we are not locked in a literal or comment
firstQuoteChar = 'i'
firstCommentChar = 'i'
# Initialize the variable that indicates that the first character of the line is a comment character
commentLockedFirstChar = False
# Initialize the variables to keep track of the previous space and next space index
prevspaceIndex = -1
nextspaceIndex = 0
# Initialize the variables to keep track of the previous quote and next quote index
prevquoteIndex = 0
nextquoteIndex = 0
# Initialize the variable to keep track of the next parantheses index
nextparanthesesIndex = 0
# Initialize the variable to keep track of whether we have reached a character in the line
charReached = False
# Initialize the string which prints out the code with excess spaces and comments removed
excessRemoved = ''
# Initialize the variable to check if we need to remove the repeated space after a space
removeSpace = False

# Function to check if a string is a number: https://stackoverflow.com/questions/40097590/detect-whether-a-python-string-is-a-number-or-a-letter
def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

# Open the file and read the lines
with open("test.py", "r") as file:
    for line in file:
        # Ensure that charReached and commentLockedFirstChar are set to False at the beginning of each line
        charReached = False
        commentLockedFirstChar = False
        for i, char in enumerate(line):
            # Ensure that removeSpace is set to False at the beginning of each character
            removeSpace = False
            # Check if we are not in a literal or comment
            if literalLocked == False and commentLocked == False:
                if not charReached and (char != ' ' and char != '\n' and char != '#'):
                    charReached = True
                # Check if we have reached a comment character. If we have, set commentLocked to True and increment the comment count
                if (char == '#' and firstCommentChar == 'i'):
                    commentLocked = True
                    # If comment is the first character of the line, we will not output the newline. <- This logic is seen later
                    if i == 0:
                        commentLockedFirstChar = True
                    firstCommentChar = char
                    cCount += 1
                    if char not in cList:
                        cList.append(char)
                # Check if we have reached an operator.
                elif (  char == '+' or char == '-' or char == '*' or char == '/' or char == '=' or
                        char == '<' or char == '>' or char == '%' or char == '&' or char == '|' or
                        char == '^' or char == '~' or char == '!' or char == '?' or char == '@' or
                        char == '#' or char == '$' or char == '`' or char == '++' or char == '--' or
                        char == '==' or char == '!=' or char == '<=' or char == '>=' or char == '<<' or
                        char == '>>' or char == '&&' or char == '||' or char == '+=' or char == '-=' or
                        char == '*=' or char == '/=' or char == '%=' or char == '&=' or char == '|=' or
                        char == '^=' or char == '>>=' or char == '<<=' or char == '>>>' or char == '>>>=' or
                        char == '->' or char == '=>'):
                    oCount += 1
                    if char not in oList:
                        oList.append(char)
                # Check if we have reached a separator
                elif (char in string.punctuation and char != '"' and char != "'"):
                    sCount += 1
                    if char not in sList:
                        sList.append(char)
                    # Check if there is a keyword or identifier before the parantheses for a function call
                    if (char == '('):
                        nextparanthesesIndex = i
                        for c in line[prevspaceIndex + 1:nextparanthesesIndex]:
                            koriString = koriString + c
                        if keyword.iskeyword(koriString) or koriString == 'print':
                            kCount += 1
                            if koriString not in kList:
                                kList.append(koriString)
                        elif koriString.isidentifier():
                            iCount += 1
                            if koriString not in iList:
                                iList.append(koriString)
                        koriString = ''
                # Utilize space to select words and determine if they are keywords or identifiers
                elif (char == ' '):
                    nextspaceIndex = i
                    for c in line[prevspaceIndex + 1:nextspaceIndex]:
                        koriString = koriString + c
                    prevspaceIndex = nextspaceIndex
                    if keyword.iskeyword(koriString) or koriString == 'print':
                        kCount += 1
                        if koriString not in kList:
                            kList.append(koriString)
                    elif koriString.isidentifier():
                        iCount += 1
                        if koriString not in iList:
                            iList.append(koriString)
                    koriString = ''
                    # Check for repeated spaces and remove them
                    if line[i - 1] == ' ':
                        removeSpace = True
                # Check if character is a number
                elif (is_number(char)):
                    lCount += 1
                    if char not in lList:
                        lList.append(char)
            # Check if we are in a comment
            elif literalLocked == False and commentLocked == True:
                if (char == '\n'):
                    # Begin resetting the variables for the next line
                    commentLocked = False
                    firstCommentChar = 'i'
                    prevspaceIndex = -1
                    # Logic referenced from earlier to remove the newline if the comment was the first character of the line
                    if commentLockedFirstChar:
                        charReached = False
            # Check if we are in not in a comment and maybe a literal or not (Ambiguity necessary to account for first and second quotes)
            if commentLocked == False:
                if (char == '"' or char == "'"):
                    if (firstQuoteChar == char):
                        # Unlock us from the literal and store the string literal
                        nextquoteIndex = i
                        for c in line[prevquoteIndex:nextquoteIndex + 1]:
                            stringLiteral = stringLiteral + c
                        if stringLiteral not in lList:
                            lList.append(stringLiteral)
                        literalLocked = False
                        firstQuoteChar = 'i'
                    elif (firstQuoteChar == 'i'):
                        # Lock us in a literal, log the first quote character, and increment the literal count
                        prevquoteIndex = i
                        literalLocked = True
                        firstQuoteChar = char
                        lCount += 1
                # Add character to final output string
                if charReached and not (i == 0 and char == '\n') and not removeSpace:
                    excessRemoved = excessRemoved + char

print("\n", excessRemoved)
print("\nCOUNTS")
print("Keywords: ", kCount)
print("Identifiers: ", iCount)
print("Literals: ", lCount)
print("Operators: ", oCount)
print("Separators: ", sCount)
print("Comments: ", cCount)
print("\nLISTS")
print("Keywords: ", kList)
print("Identifiers: ", iList)
print("Literals: ", lList)
print("Operators: ", oList)
print("Separators: ", sList)
print("Comments: ", cList)
print("\nTOTAL TOKENS")
print(kCount + iCount + lCount + oCount + sCount + cCount)