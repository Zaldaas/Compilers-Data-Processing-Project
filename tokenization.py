import keyword
import string

kCount = 0
iCount = 0
koriString = ''
lCount = 0
firstQuoteChar = 'i'
literalLocked = True
oCount = 0
sCount = 0
cCount = 0
firstCommentChar = 'i'
commentLocked = True
prevspaceIndex = 0
nextspaceIndex = 0

with open("test.py", "r") as file:
    for line in file:
        for char in file:
            print(char)
            if (char == '#' and firstCommentChar == 'i'):
                commentLocked = True
                firstCommentChar = char
                cCount += 1
            elif (char in string.punctuation):
                sCount += 1
            elif (char == '+' or char == '-' or char == '*' or char == '/' or char == '=' or
                    char == '<' or char == '>' or char == '%' or char == '&' or char == '|' or
                    char == '^' or char == '~' or char == '!' or char == '?' or char == '@' or
                    char == '#' or char == '$' or char == '`' or char == '++' or char == '--' or
                    char == '==' or char == '!=' or char == '<=' or char == '>=' or char == '<<' or
                    char == '>>' or char == '&&' or char == '||' or char == '+=' or char == '-=' or
                    char == '*=' or char == '/=' or char == '%=' or char == '&=' or char == '|=' or
                    char == '^=' or char == '>>=' or char == '<<=' or char == '>>>' or char == '>>>=' or
                    char == '->' or char == '=>'):
                oCount += 1
            elif ((char == '"' or char == "'") and firstQuoteChar == 'i'):
                if (char == firstQuoteChar):
                    literalLocked = False
                    firstQuoteChar = 'i'
                else:
                    literalLocked = True
                    firstQuoteChar = char
                    lCount += 1
            elif (char == ' '):
                nextspaceIndex = char
                for i in range(prevspaceIndex + 1, nextspaceIndex):
                    koriString.insert(0, char)
                prevspaceIndex = nextspaceIndex
                if keyword.iskeyword(koriString):
                    kCount += 1
                elif koriString.isidentifier():
                    iCount += 1
            elif (char == '\n'):
                commentLocked = False
                firstCommentChar = 'i'
            else:
                lCount += 1

print("Keywords: ", kCount)
print("Identifiers: ", iCount)
print("Literals: ", lCount)
print("Operators: ", oCount)
print("Separators: ", sCount)
print("Comments: ", cCount)