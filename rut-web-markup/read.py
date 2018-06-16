class Read:

    specials = [".", "#", "^", "|", "(", ")", "\"", "{", "}", "$", "*", "_"]

    def __init__(self, filename):
        self.filename = filename
        self.reader = open(filename, "r")
        self.line = self.reader.readline()
        self.p = 0
        self.use_last = False
        self.last = ""

    def next_token(self):

        # If needed to rereturn value
        if self.use_last:
            self.use_last = False
            return self.last

        # If pointer is past line, get new line
        if self.p >= len(self.line):
            self.line = self.reader.readline()
            self.p = 0
        
        # If end of file, return empty string
        if self.line == "":
            return ""

        # Initialize new last
        self.last = ""

        while self.p < len(self.line):

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

        # Reached end of line; return what was found
        return self.last

    def is_special(self, token):
        for x in self.specials:
            if x == token:
                return True
        return False

    def undo_token(self):
        self.use_last = True