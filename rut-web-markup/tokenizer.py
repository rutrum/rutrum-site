# practice reading from file

file = open("test.txt", "r")
tokens = open("tokens.txt", "w")

specials = [".", "#", "^", "|", "(", ")", "\"", "{", "}", "$", "*", "_"] 

def tokenize():
    for line in file:
        # ignore comments
        if is_comment(line):
            continue
        # divide up the words
        words = line.split()
        for word in words:
            split_word(word)

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
    if word == "":
        return
    for x in range(len(word)):
        for y in specials:
            if (word[x] == y):
                if (x != 0):
                    tokens.write(word[0:x] + "\n")
                tokens.write(word[x] + "\n")
                if (x != len(word)):
                    split_word(word[x + 1:len(word)])
                return
    tokens.write(word + "\n")

                
tokenize()

file.close()
tokens.close()

# file = open("test.txt", "r")
# output = open("output.txt", "w")

# for line in file:
#     words = line.split()
#     for word in words:
#         output.write(word)
#         output.write("\n")
    
# file.close()
# output.close()

# def printhey(string):
#     print string
#     return string

    

# name = printhey("what")

# print "hey", name