from ViewManager import viewManager
from Component import Component
import Utils.utils as utils


class TitleBar(Component):

    def __init__(self, name):
        super().__init__(name)
        self.addShortcut("C", utils.clearCache)

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
