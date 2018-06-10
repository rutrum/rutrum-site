file = open("test.txt", "r")
tokens = open("tokens.txt", "w")
output = open("test.html", "w")

specials = [".", "#", "^", "|", "(", ")", "\"", "{", "}", "$", "*", "_"]

# spl create token files into words and tokens
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
                    tokens.write(word[0:x] + "\n")
                # add special character
                tokens.write(word[x] + "\n")
                # add words after special character recursively
                if (x != len(word)):
                    split_word(word[x + 1:len(word)])
                return
    # if no delimiters were found
    tokens.write(word + "\n")

def parser():
    for token in tokens:
        token = token.strip() # remove newline
        index = special(token)
        if index != -1:
            # switch
            False
        else:
            # must be a tag name
            start_tag(token)

def start_tag(name):
    print "<" + name + ">"

def special(token):
    for x in specials:
        if (x == token):
            return x
    return -1

# create token file
tokenizer()

tokens.close()
tokens = open("tokens.txt", "r")

# create html file
parser()

# close file readers
file.close()
tokens.close()

# delete tokens.txt
# import os
# os.remove("tokens.txt")