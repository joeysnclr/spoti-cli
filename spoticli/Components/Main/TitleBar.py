from spoticli.Components.Main.ViewManager import viewManager
from spoticli.Components.Templates.Component import Component


class TitleBar(Component):

    def __init__(self, name):
        super().__init__(name)

    def output(self, lines):
        outputLines = []
        mainView = viewManager.mainView
        mainViewName = mainView.name
        title = mainViewName
        if hasattr(mainView, "pages"):
            title += f" {mainView.currPage}/{mainView.pages}"
        outputLines.append(title)
        return outputLines
