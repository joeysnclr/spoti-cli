from Component import Component


class Log(Component):

    def __init__(self):
        super().__init__("log")
        self.logs = []

    def output(self, lines):
        if self.logs == []:
            return [""]
        return [self.logs[-1]]

    def log(self, info):
        self.logs.append(info)

log = Log()
