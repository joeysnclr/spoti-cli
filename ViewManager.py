from blessed import Terminal
from Component import Component
import Utils.utils as utils


class ViewManager(object):

    def __init__(self, term):
        self.term = term
        self.running = True
        self.title = None
        self.mainView = None
        self.player = None
        self.logOutput = None
        self.previousMainViews = []
        self.globalShortcuts = {
            "q": self.quit,
            "C": utils.clearCache,
            "h": self.previousMainView
        }

    def start(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            # clear the screen
            print(self.term.home + self.term.clear)
            # render loop
            while self.running:
                # wait for key
                key = self.term.inkey(timeout=.03333)
                # reset components in case mainView has changed
                self.components = [self.title, self.mainView, self.player, self.logOutput]
                # shortcuts
                self.shortcuts(key)
                # rendering
                self.render()
            print(self.term.home + self.term.clear)

    def shortcuts(self, key):
        if key:
            if key.is_sequence:
                key = key.name
            # run global shortcuts
            if key in self.globalShortcuts:
                self.globalShortcuts[key]()
            # run component specific shortcuts
            for component in self.components:
                component.handleShortcut(key)

    def render(self):
        # calculate # of lines for each component
        height = self.term.height - 1
        titleHeight = 2
        playerHeight = 5
        logOutputHeight = 1
        mainViewHeight = height - titleHeight - playerHeight - logOutputHeight
        heights = [titleHeight, mainViewHeight, playerHeight, logOutputHeight]
        # gather output for each component
        componentOutputs = []
        for height, component in zip(heights, self.components):
            componentOutputs.append(component.output(height))
        # clear screen and output each component
        print(self.term.home + self.term.clear_eol)
        for output in componentOutputs:
            for line in output:
                print(self.term.clear_eol + line)

    def setMainView(self, component):
        if self.mainView != None:
            self.previousMainViews.append(self.mainView)
        self.mainView = component

    def previousMainView(self):
        if len(self.previousMainViews) > 0:
            self.mainView = self.previousMainViews.pop()

    def quit(self):
        self.running = False
        quit()


viewManager = ViewManager(Terminal())
