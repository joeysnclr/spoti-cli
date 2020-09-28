from spoticli.Utils.utils import shortcuts

class Component(object):

    def __init__(self, name):
        self.name = name
        self.shortcuts = {}

    def update(self, lines):
        pass

    def output(self, lines):
        outputLines = []
        for i in range(lines):
            outputLines.append(self.name)
        return outputLines

    def addShortcut(self, key, function):
        self.shortcuts[key] = function

    def handleInput(self, key):
        action = shortcuts.getAction(key)
        if action in self.shortcuts:
            self.shortcuts[action]()
