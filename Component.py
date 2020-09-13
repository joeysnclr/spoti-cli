class Component(object):

    def __init__(self, name, shortcuts={}):
        self.name = name
        self.shortcuts = shortcuts

    def update(self):
        pass

    def output(self, lines):
        outputLines = []
        for i in range(lines):
            outputLines.append(self.name)
        return outputLines

    def handleShortcut(self, key):
        if key in self.shortcuts:
            self.shortcuts[key]()
