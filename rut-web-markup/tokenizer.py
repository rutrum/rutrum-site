file = open("test.rutwm", "r")
tokens_file = open("tokens.txt", "w")
output = open("test.html", "w")

specials = [".", "#", "^", "|", "(", ")", "\"", "{", "}", "$", "*", "_"]

tokens = []
current_token = 0
tabs = 0
last_token = ""

# --- tokenizer

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

# --- parser

def initialize_tokens():
    global tokens 
    tokens = tokens_file.readlines()

def undo_token(token):
    global last_token
    last_token = token

def next_token():
    global current_token
    global tokens
    global last_token

    if last_token != "":
        to_return = last_token
        last_token = ""
        return to_return

    if current_token == len(tokens):
        return ""

    token = tokens[current_token].strip()
    current_token += 1
    return token

def compile_next():
    token = next_token()
    if token == "":
        return ""

    if is_special(token):
        if token == "{":
            # should be compiling a start tag with class and id props
            start_tag()
        elif token == "}":
            end_tag()
        elif token == ".":
            global classes
            token = next_token()
            classes.append(token)
        elif token == "#":
            global ids
            token = next_token()
            ids.append(token)
        elif token == "|":
            add_attribute()
        elif token == "^":
            add_style()
        elif token == "\"":
            compile_string()
    else:
        # add tag name to global
        global tag_name
        add_tag_name(token)

# --- Tag globals

tag_names = []
classes = []
ids = []

attributes = []
styles = []

class Attribute:
    name = ""
    value = ""

class Style:
    name = ""
    value = ""

# --- Tag creation

def start_tag():
    global classes
    global ids
    global attributes
    tag = "<" + get_tag_name()

    if len(classes) > 0:
        tag += " class=\""
        while len(classes) > 1:
            tag += classes.pop(0) + " "
        tag += classes.pop(0) + "\""
    
    if len(ids) > 0:
        tag += " id=\""
        while len(ids) > 1:
            tag += ids.pop(0) + " "
        tag += ids.pop(0) + "\""
    
    if len(styles) > 0:
        tag += " style=\""
        s = styles.pop(0)
        tag += s.name + ":" + s.value + ";"
        while len(styles) > 0:
            s = styles.pop(0)
            tag += " " + s.name + ":" + s.value + ";"
        tag += "\""

    while len(attributes) > 0:
        a = attributes.pop(0)
        if a.value == "":
            tag += " " + a.name
        else:
            tag += " " + a.name + "=\"" + a.value + "\""
            

    tag += ">\n"
    output.write(get_tabs() + tag)
    inc_tabs()

def end_tag():
    dec_tabs()
    output.write(get_tabs() + "</" + pop_tag_name() + ">\n")

def add_tag_name(name):
    global tag_names
    tag_names.append(name)

def get_tag_name():
    global tag_names
    if (len(tag_names) > 0):
        return tag_names[-1]
    return ""

def pop_tag_name():
    global tag_names
    if (len(tag_names) > 0):
        return tag_names.pop(-1)
    return ""

def compile_string():
    token = next_token()
    if (token != "\""):
        output.write(get_tabs() + token)
        token = next_token()
    while token != "\"":
        output.write(" " + token)
        token = next_token()
    output.write("\n")

def add_attribute():
    a = Attribute()
    a.name = next_token()
    maybe = next_token()
    if maybe != "(":
        attributes.append(a)
        # need to reset next_token
        undo_token(maybe)
        return
    
    token = next_token()
    # no space
    if token != ")":
        a.value += token
        token = next_token()
    # need leading space
    while token != ")":
        a.value += " " + token
        token = next_token()
    attributes.append(a)

def add_style():
    s = Style()
    s.name = next_token()
    if next_token() != "(":
        print "ERROR expectected '('"
    
    token = next_token()
    # no space
    if token != ")":
        s.value += token
        token = next_token()
    # need leading space
    while token != ")":
        s.value += " " + token
        token = next_token()
    styles.append(s)

# --- Controls the tabing in html output

def get_tabs():
    t = ""
    global tabs
    for x in range(tabs):
        t += "    "
    return t

def inc_tabs():
    global tabs
    tabs += 1

def dec_tabs():
    global tabs
    tabs -= 1

def is_special(token):
    for x in specials:
        if x == token:
            return True
    return False

# --- Main

# create token file
tokenizer()

tokens_file.close()
tokens_file = open("tokens.txt", "r")

current_token = 0
initialize_tokens()

# starts the creation of html file
while compile_next() != "":
    0

# close file readers
file.close()
tokens_file.close()

# delete tokens_file.txt
# import os
# os.remove("tokens.txt")