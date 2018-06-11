file = open("test.txt", "r")
tokens_file = open("tokens.txt", "w")
output = open("test.html", "w")

specials = [".", "#", "^", "|", "(", ")", "\"", "{", "}", "$", "*", "_"]

tokens = []
current_token = 0

# create token files into words and tokens_file
def tokenizer():
    for line in file:
        # ignore comments
        if is_comment(line):
            continue
        # divide up the words
        words = line.split()
        for word in words:
            split_word(word)

# determines if a line of text is a comment
def is_comment(line):
    line = line.strip()
    if len(line) == 0:
        return True
    if len(line) > 1:
        if line[0] == "/" and line[1] == "/":
            return True
    return False

# break up words by special characters
# for each character in word, does it match a special character?
def split_word(word):
    # if empty, base case for recursion
    if word == "":
        return
    # for every character in word, compare it to every delimiter
    for x in range(len(word)):
        for y in specials:
            if (word[x] == y):
                # add word before special character
                if (x != 0):
                    tokens_file.write(word[0:x] + "\n")
                # add special character
                tokens_file.write(word[x] + "\n")
                # add words after special character recursively
                if (x != len(word)):
                    split_word(word[x + 1:len(word)])
                return
    # if no delimiters were found
    tokens_file.write(word + "\n")

def initialize_tokens():
    global tokens 
    tokens = tokens_file.readlines()

def next_token():
    global current_token
    global tokens

    if current_token == len(tokens):
        return ""

    token = tokens[current_token].strip()
    current_token += 1
    return token

def compile_next():
    token = next_token()
    if token == "":
        return

    if is_special(token):
        if token == "{":
            # should be compiling a start tag with class and id props
            compile_next()
        elif token == "}":
            return
        elif token == "\"":
            compile_string()
    else:
        start_tag(token)
        compile_next()
        end_tag(token)
        compile_next()

def compile_string():
    token = next_token()
    while token != "\"":
        token = next_token()

def start_tag(name):
    print "<" + name + ">"

def end_tag(name):
    print "</" + name + ">"

def is_special(token):
    for x in specials:
        if x == token:
            return True
    return False

# create token file
tokenizer()

tokens_file.close()
tokens_file = open("tokens.txt", "r")

current_token = 0
initialize_tokens()

# starts the creation of html file
compile_next()

# close file readers
file.close()
tokens_file.close()

# delete tokens_file.txt
# import os
# os.remove("tokens.txt")