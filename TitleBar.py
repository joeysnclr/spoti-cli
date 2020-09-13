from ViewManager import viewManager
from Component import Component


class TitleBar(Component):

    def __init__(self, name, shortcuts={}):
        Component.__init__(self, name, shortcuts)

    def output(self, lines):
        outputLines = []
        mainView = viewManager.mainView
        mainViewName = mainView.name
        title = mainViewName
        if hasattr(mainView, "pages"):
            title += f" {mainView.currPage}/{mainView.pages}"

        outputLines.append(title)
        for i in range(lines - 1):
            outputLines.append("")
        return outputLines
