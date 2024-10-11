import re
from tabulate import tabulate

keywords=["def", "print", "if", "return"]
operators = ["=", "+", "=="]
delimiters = ["(", ")", ",", ":"]

kCount = 0
oCount = 0
dCount = 0
lCount = 0
iCount = 0
keywordsFound=[]
operatorsFound=[]
delimitersFound=[]
literalsFound=[]
identifiersFound=[]
def clean_py_file(input_file, output_file):
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            for line in infile:
                stripped_line = line.strip()  # Remove leading/trailing whitespace
                # Skip comments and completely blank lines
                if not stripped_line or stripped_line.startswith("#"):
                    continue
                if stripped_line.__contains__("#"):
                    stripped_line = stripped_line[:stripped_line.find('#')]

                # Remove spaces around operators, commas, colons, and keywords
                cleaned_line = re.sub(r'\s*([+*/-])\s*', r' \1 ', stripped_line)  # Remove spaces around operators
                cleaned_line = re.sub(r'\s*([,:])\s*', r'\1 ', cleaned_line)  # Remove spaces around separators
                cleaned_line = re.sub(r'\s+', ' ', cleaned_line)  # Reduce multiple spaces to a single space
                
                # Remove spaces before and after keywords 
                keywords = ["def", "return", "print", "if", "else", "elif", "for", "while", "in", "and", "or", "not"]
                cleaned_line = cleaned_line.strip()
                outfile.write(cleaned_line + "\n")

        print(f"Processed code written to {output_file}")
    
    except FileNotFoundError:
        print(f"The file at {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def readCleanedFile(clean_file):
    global kCount
    global oCount
    global dCount
    global lCount
    global iCount
    global keywordsFound
    global operatorsFound
    global delimitersFound
    global literalsFound
    global identifiersFound
    with open(clean_file, "r") as file:
        for line in file:
            strings = re.findall(r'"(.*?)"', line)
            for string in strings:
                lCount = lCount + 1
                if string not in keywordsFound:
                    literalsFound.append(string)
                line = line.replace(string, '',1)
                line = line.replace('"', '')

            nums = re.findall(r'\b\d+\b', line)
            for num in nums:
                lCount = lCount + 1
                if num not in literalsFound:
                    literalsFound.append(num)
                line = line.replace(num, '',1)
                #line = line.replace('"', '')

            for keyword in keywords:
                if keyword in line:
                    kCount = kCount + 1
                    if keyword not in keywordsFound:
                        keywordsFound.append(keyword)
                    line = line.replace(keyword,'',1)

            identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', line)
            for identifier in identifiers:
                if identifier not in keywords:
                    iCount = iCount + 1
                    if identifier not in identifiersFound:
                            identifiersFound.append(identifier)
                    line = line.replace(identifier,'',1)

            for operator in operators:
                if operator in line:
                    oCount = oCount + 1
                    if operator not in operatorsFound:
                        operatorsFound.append(operator)
                    line = line.replace(operator,'',1)

            delimiterPresent = True
            while delimiterPresent:
                delimiterPresent = False
                for delimiter in delimiters:
                    if delimiter in line:
                        dCount = dCount + 1
                        if delimiter not in delimitersFound:
                            delimitersFound.append(delimiter)
                        line = line.replace(delimiter, '',1)
                        delimiterPresent = True

input_file = "CPSC323-Project1/test.py"  
output_file = "CPSC323-Project1/cleaned.py"  # Output file 

# Call the function to clean the Python file
clean_py_file(input_file, output_file)
readCleanedFile(output_file)

with open(output_file, "r") as file:
        for line in file:
            print(line)
            
print("Keyword count: " , kCount)
print ("Operator count: " , oCount)
print ("Delimiter count: " , dCount)
print ("literal count: " , lCount)
print("identifier count: ", iCount)

data = [
    ["Keywords", keywordsFound],
    ["Operators", operatorsFound],
    ["Delimiters", delimitersFound],
    ["Literals", literalsFound],
    ["Identifiers", identifiersFound]
]
table = tabulate(data, headers=["Category", "Tokens"], tablefmt="grid")
print(table)