import keyword
import string

kCount = 0
iCount = 0
koriString = ''
lCount = 0
firstQuoteChar = 'i'
literalLocked = False
oCount = 0
sCount = 0
cCount = 0
firstCommentChar = 'i'
commentLocked = False
prevspaceIndex = -1
nextspaceIndex = 0
nextparanthesesIndex = 0

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True


def main():
    with open("test.py", "r") as file:
        # Change enumerate back
        for line in file:
            for i, char in enumerate(line):
                print(char, end='')
                if literalLocked == False and commentLocked == False:
                    if (char == '#' and firstCommentChar == 'i'):
                        commentLocked = True
                        firstCommentChar = char
                        cCount += 1
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
                    elif (char in string.punctuation and char != '"' and char != "'"):
                        sCount += 1
                        if (char == '('):
                            nextparanthesesIndex = i
                            for c in line[prevspaceIndex + 1:nextparanthesesIndex]:
                                koriString = koriString + c
                            if keyword.iskeyword(koriString) or koriString == 'print':
                                kCount += 1
                            elif koriString.isidentifier():
                                iCount += 1
                            koriString = ''
                    elif (char == ' '):
                        nextspaceIndex = i
                        for c in line[prevspaceIndex + 1:nextspaceIndex]:
                            koriString = koriString + c
                        prevspaceIndex = nextspaceIndex
                        if keyword.iskeyword(koriString) or koriString == 'print':
                            kCount += 1
                        elif koriString.isidentifier():
                            iCount += 1
                        koriString = ''
                    elif (is_number(char)):
                        lCount += 1
                elif literalLocked == False and commentLocked == True:
                    if (char == '\n'):
                        commentLocked = False
                        firstCommentChar = 'i'
                        prevspaceIndex = -1
                if commentLocked == False:
                    if (char == '"' or char == "'"):
                        if (firstQuoteChar == char):
                            literalLocked = False
                            firstQuoteChar = 'i'
                        elif (firstQuoteChar == 'i'):
                            literalLocked = True
                            firstQuoteChar = char
                            lCount += 1

print("\nKeywords: ", kCount)
print("Identifiers: ", iCount)
print("Literals: ", lCount)
print("Operators: ", oCount)
print("Separators: ", sCount)
print("Comments: ", cCount)