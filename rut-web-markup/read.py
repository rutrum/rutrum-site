class Read:

    specials = [".", "#", "^", "|", "(", ")", "\"", "{", "}", "$", "*", "_"]

    def __init__(self, filename):
        self.filename = filename
        self.reader = open(filename, "r")
        self.line = self.reader.readline()
        self.p = 0
        self.use_last = False
        self.last = ""
        self.found_quotes = False

    def next_token(self):

        # If needed to rereturn value
        if self.use_last:
            self.use_last = False
            return self.last

        # If expected token is a string (or end of one)
        if self.last == "\"":
            if self.found_quotes:
                self.found_quotes = False
            else:
                self.found_quotes = True
                self.last = ""
                return self.return_string("\"")

        # If expected token is a parameter
        if self.last == "(":
            self.last = ""
            return self.return_string(")")

        # If pointer is past line, get new line
        if self.p >= len(self.line) - 1: # -1 ignores \n
            self.line = self.reader.readline()
            self.p = 0
        
        # If end of file, return empty string
        if self.line == "":
            return ""

        # Initialize new last
        self.last = ""

        while self.p < len(self.line) - 1:

            char = self.line[self.p]

            if self.is_special(char):
                if self.last == "":
                    # Only seen special
                    self.p += 1
                    self.last = char
                    return char
                # Already read non-special characters
                return self.last

            elif char == " ":
                self.p += 1
                # Ignores tabs/spaces at beginning of lines
                if self.last == "":
                    continue
                return self.last

            else:
                # Character is not special or space
                self.last += char
                self.p += 1

        # If returning trailing spaces, try again with next line
        if self.last == "":
            return self.next_token()

        # Reached end of line; return what was found
        return self.last

    def return_string(self, expected):
        char = self.line[self.p]
        while (char != expected and self.p < len(self.line) - 1):
            self.last += char
            self.p += 1
            char = self.line[self.p]
        return self.last

    # Is the character a special character?
    def is_special(self, char):
        for x in self.specials:
            if x == char:
                return True
        return False

    def undo_token(self):
        self.use_last = True