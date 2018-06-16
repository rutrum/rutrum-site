class Tag:
    
    class Pair:
        def __init__(self, name, value):
            self.name = name
            self.value = value

    def __init__(self, name):
        self.name = name
        self.ids = []
        self.classes = []
        self.styles = []
        self.attributes = []

    # Functions that add attributes

    def add_id(self, name):
        self.classes.append(name)

    def add_class(self, name):
        self.classes.append(name)
    
    def add_style(self, name, value):
        self.styles.append(Pair(name, value))
    
    def add_attribute(self, name, value):
        self.attributes.append(Pair(name, value))

    # Functions that write tags

    def write_classes(self):
        if len(self.classes) == 0:
            return ""
        s = " class=\"" + self.classes[0]
        for x in range(1, len(self.classes)):
            s += " " + self.classes[x]
        s += "\""
        return s

    def write_ids(self):
        if len(self.ids) == 0:
            return ""
        s = " id=\"" + self.ids[0]
        for x in range(1, len(self.ids)):
            s += " " + self.ids[x]
        s += "\""
        return s

    def write_styles(self):
        if len(self.styles) == 0:
            return ""
        s = " style=\"" + self.styles[0].name + ":" + self.styles[0].value + ";"
        for x in range(1, len(self.styles)):
            s += self.styles[x].name + ":" + self.styles[x].value + ";"
        s += "\""
        return s

    def write_attributes(self):
        if len(self.styles) == 0:
            return ""
        for x in range(0, len(self.styles)):
            s += " " + self.attributes[x].name + "=\"" + self.attributes[x].value + "\""
        return s

    def get_start_tag(self):
        tag = "<" + self.name
        tag += self.write_classes()
        tag += self.write_ids()
        tag += self.write_styles()
        tag += self.write_attributes()
        tag += ">"
        return tag

    def get_end_tag(self):
        return "</" + self.name + ">"