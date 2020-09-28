from blessed import Terminal
from Components.Templates.Component import Component
from Components.Main.HelpMenu import HelpMenu
from Utils.utils import spotifyCache


class ViewManager(Component):

    def __init__(self, term):
        super().__init__("View Manager")
        self.term = term
        self.running = True
        self.title = None
        self.mainView = None
        self.player = None
        self.logOutput = None
        self.previousMainViews = []
        self.addShortcut("quit", self.quit)
        self.addShortcut("clearCache", spotifyCache.clear)
        self.addShortcut("prevView", self.previousMainView)
        self.addShortcut("helpMenu", self.showHelpMenu)

    def start(self):
        with self.term.cbreak(), self.term.hidden_cursor(), self.term.fullscreen():
            # clear the screen
            print(self.term.home + self.term.clear)
            # render loop
            while self.running:
                # wait for key
                key = self.term.inkey(timeout=.03333)
                # key = self.term.inkey(timeout=5)
                # reset components in case mainView has changed
                self.components = [self.title, self.mainView, self.player, self.logOutput]
                self.componentHeights = self.calcHeights()
                # shortcuts
                self.keyPress(key)
                # updating
                self.update()
                # rendering
                self.render()

    def keyPress(self, key):
        if key:
            if key.is_sequence:
                key = key.name
            super().handleInput(key)
            # run component specific shortcuts
            for component in self.components:
                component.handleInput(key)

    def update(self):
        for height, component in zip(self.componentHeights, self.components):
            component.update(height)

    def render(self):
        # gather output for each component
        componentOutputs = []
        for height, component in zip(self.componentHeights, self.components):
            output = component.output(height)
            while len(output) < height:
                output.append("")
            componentOutputs.append(output)

        # clear screen and output each component
        print(self.term.home, end="")
        for output in componentOutputs:
            for line in output:
                print(self.term.clear_eol + line)

    def calcHeights(self):
        # calculate # of lines for each component
        height = self.term.height - 1
        titleHeight = 2
        playerHeight = 3
        logOutputHeight = 1
        mainViewHeight = height - titleHeight - playerHeight - logOutputHeight
        heights = [titleHeight, mainViewHeight, playerHeight, logOutputHeight]
        return heights

    def setMainView(self, component):
        if self.mainView != None:
            self.previousMainViews.append(self.mainView)
        self.mainView = component

    def previousMainView(self):
        if len(self.previousMainViews) > 0:
            self.mainView = self.previousMainViews.pop()

    def showHelpMenu(self):
        helpMenu = HelpMenu()
        self.setMainView(helpMenu)

    def quit(self):
        self.running = False


viewManager = ViewManager(Terminal())
