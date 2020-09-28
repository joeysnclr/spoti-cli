from spoticli.Components.Templates.Component import Component


class Log(Component):

    def __init__(self):
        super().__init__("log")
        self.addShortcut("toggleLog", self.toggleDisplay)
        self.logs = []
        self.display = False

    def output(self, lines):
        if self.logs == [] or not self.display:
            return [""]
        return [self.logs[-1]]

    def log(self, info):
        self.logs.append(info)

    def toggleDisplay(self):
        self.display = not self.display

log = Log()
