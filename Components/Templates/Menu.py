import math
from ViewManager import viewManager
from Components.Templates.Component import Component
from Components.Main.Player import player

term = viewManager.term


class MenuItem(Component):

    def __init__(self, name):
        super().__init__(name)
        self.addShortcut("l", self.onSelect)
        self.addShortcut("KEY_ENTER", self.onSelect)
        self.isActive = False

    def update(self):
        pass

    def setActive(self, active):
        self.isActive = active

    def onSelect(self):
        pass
        # viewManager.mainView.name = self.name

    def output(self, lines):
        if self.isActive:
            return term.reverse + self.name + term.normal
        return self.name


class Menu(Component):

    def __init__(self, name, items):
        super().__init__(name)
        self.addShortcut("j", self.positionDown)
        self.addShortcut("k", self.positionUp)
        self.addShortcut("n", self.nextPage)
        self.addShortcut("N", self.prevPage)
        self.addShortcut("g", self.positionFirst)
        self.addShortcut("G", self.positionLast)
        self.items = items
        self.currItems = []
        self.position = 0
        self.currPage = 1

    def update(self):
        pass

    def handleShortcut(self, key):
        if key in self.shortcuts:
            self.shortcuts[key]()
        # handle active item shortcut
        if len(self.currItems) > 0:
            self.currItems[self.position].handleShortcut(key)

    def output(self, lines):
        self.initPaging(lines)

        # set all items to not active
        for item in self.items:
            item.setActive(False)

        # set current position item to active
        self.currItems[self.position].setActive(True)

        # get outputs
        outputLines = []
        for item in self.currItems:
            outputLines.append(item.output(1))

        while len(outputLines) < lines:
            outputLines.append("")
        return outputLines

    def initPaging(self, lines):
        self.perPage = lines
        self.pages = math.ceil(len(self.items) / self.perPage)
        if self.currPage > self.pages or self.currPage < 1:
            self.currPage = 1
            self.position = 0
        startIndex = (self.currPage - 1) * self.perPage
        endIndex = self.currPage * self.perPage
        currItems = self.items[startIndex:endIndex]
        self.currItems = currItems
        if self.position > len(self.currItems) - 1:
            self.position = 0

    def changePage(self, n):
        nextPage = self.currPage + n
        if nextPage < 1 or nextPage > self.pages:
            return
        self.currPage = nextPage

    def nextPage(self):
        self.changePage(1)

    def prevPage(self):
        self.changePage(-1)

    def changePosition(self, n):
        newPosition = self.position + n
        if newPosition < 0 or newPosition > len(self.currItems) - 1:
            return
        self.position = newPosition

    def positionDown(self):
        self.changePosition(1)

    def positionUp(self):
        self.changePosition(-1)

    def positionFirst(self):
        self.position = 0

    def positionLast(self):
        self.position = len(self.currItems) - 1
