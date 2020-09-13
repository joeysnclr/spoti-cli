import math
from Component import Component
from ViewManager import ViewManager


class MenuItem(Component):

    def __init__(self, name, shortcuts={}):
        shortcuts["m"] = self.changeName
        Component.__init__(self, name, shortcuts)
        self.isActive = False

    def setActive(self, active):
        self.isActive = active

    def changeName(self):
        self.name = "shortcut"

    def output(self, lines):
        output = self.name
        if self.isActive:
            output += self.name
        return output


class Menu(Component):

    def __init__(self, name, shortcuts={}, items=[]):
        shortcuts["j"] = self.positionDown
        shortcuts["k"] = self.positionUp
        shortcuts["n"] = self.nextPage
        shortcuts["N"] = self.prevPage
        Component.__init__(self, name, shortcuts)
        self.items = items
        self.position = 0
        self.currPage = 1
        self.currItems = []

    def initPaging(self, lines):
        self.perPage = lines
        self.pages = math.ceil(len(self.items) / self.perPage)
        if self.currPage > self.pages or self.currPage < 1:
            self.currPage = 1
            self.position = 0
        startItems = (self.currPage - 1) * self.perPage
        endItems = startItems + self.perPage
        self.currItems = self.items[startItems:endItems]

    def setPosition(self, n):
        self.position = n

    def changePositon(self, n):
        lastPosition = self.perPage
        if self.currPage == self.pages:
            lastPosition = len(self.currItems)
        nextPosition = self.position + n
        if nextPosition >= 0 and nextPosition < lastPosition:
            self.setPosition(nextPosition)

    def positionDown(self):
        self.changePositon(1)

    def positionUp(self):
        self.changePositon(-1)

    def changePage(self, n):
        newPageNum = self.currPage + n
        if newPageNum > 0 and newPageNum <= self.pages:
            self.currPage = newPageNum
            self.setPosition(0)

    def nextPage(self):
        self.changePage(1)

    def prevPage(self):
        self.changePage(-1)

    def output(self, lines):
        output = []
        self.initPaging(lines)
        # remove active from all items
        for item in self.items:
            item.setActive(False)
        for i, item in enumerate(self.currItems):
            if i == self.position:
                item.setActive(True)
            output.append(item.output(1))

        while len(output) < lines:
            output.append("")
        return output

    def handleShortcut(self, key):
        if key in self.shortcuts:
            self.shortcuts[key]()
        for item in self.currItems:
            if item.isActive:
                item.handleShortcut(key)
