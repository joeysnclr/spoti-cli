import curses
from curses import panel
import math
import MenuBar
import utils


class Menu(object):
    def __init__(self, items, stdscreen, title, menuBar):
        # init window stuff
        self.stdscreen = stdscreen
        self.window = stdscreen.subwin(1, 1)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()
        curses.curs_set(0)

        # init some curses settings
        curses.halfdelay(8)  # set frame update in ms
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_WHITE)

        # menu data
        self.title = title
        self.menuBar = menuBar
        self.position = 0
        self.active = None
        self.items = items
        self.command = ""
        self.currPage = 1
        self.initPaging()

    def initPaging(self):
        """
        inits paging
        """
        self.winHeight = self.stdscreen.getmaxyx()[0]

        self.perPage = self.winHeight - self.menuBar.height - 2
        self.pages = math.ceil(len(self.items) / self.perPage)
        if self.currPage > self.pages:
            self.currPage = self.pages
            self.position = 0

    def getLastElem(self):
        """
        returns index of last visible element on screen
        """
        first = self.perPage * (self.currPage - 1)
        last = self.perPage * (self.currPage)
        if last > len(self.items):
            last = len(self.items)
        lastElem = last - first
        return lastElem

    def navigate(self, n):
        """
        moves selection by n
        """
        lastElem = self.getLastElem()
        nextPosition = self.position + n
        if nextPosition >= 0 and nextPosition < lastElem:
            self.position += n

    def setActive(self, i):
        """
        set active given index
        """
        self.active = i

    def displayLine(self, y, x, content, color):
        self.window.addstr(y, x, content, color)

    def display(self):
        """
        handle frame loop
        """
        self.panel.top()
        self.panel.show()
        self.window.erase()

        while True:
            # gather data to be displayed before clearing display

            width = self.stdscreen.getmaxyx()[1]
            self.initPaging()  # responsive paging
            first = self.perPage * (self.currPage - 1)
            last = self.perPage * (self.currPage)

            shownItems = []
            for index, item in enumerate(self.items):
                if index >= first and index < last:
                    formatted = item.formatMethod(item.data)
                    if item.isActive:
                        if item.isActive(item.data):
                            self.setActive(index)
                    shownItems.append((index, item, formatted))

            # set window to override old contents with new contents on next refresh
            self.window.erase()

            menuBar = self.menuBar.generateOutput(
                width, self.title, self.currPage, self.pages)
            i = 0
            for line in menuBar:
                self.displayLine(i, 0, line, curses.A_NORMAL)
                i += 1

            for index, item, formatted in shownItems:
                row = index - ((self.currPage - 1) * self.perPage)
                if row == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL
                if self.active == index:
                    if self.position == row:
                        mode = curses.color_pair(2)
                    else:
                        mode = curses.color_pair(1)

                self.displayLine(self.menuBar.height +
                                 row, 0, formatted, mode)

            # refreshes the screen
            self.window.refresh()
            curses.doupdate()

            # handles shortcuts
            key = self.window.getch()

            # handles menubar shortcuts
            if key != -1:
                for sc in self.menuBar.shortcuts:
                    if chr(key) == sc:
                        self.menuBar.shortcuts[sc]()

            # handles menu shortcuts
            if key in [108, curses.KEY_ENTER, ord("\n")]:
                index = self.position + \
                    (self.perPage * (self.currPage - 1))
                item = self.items[index]
                item.onSelectMethod(item.data)

            elif key == curses.KEY_UP or key == 107:
                self.navigate(-1)
            elif key == curses.KEY_DOWN or key == 106:
                self.navigate(1)
            elif key == 104:
                # exit submenu
                break
            elif key == 113:
                quit()
            elif key == 110:
                if self.currPage < self.pages:
                    self.position = 0
                    self.currPage += 1
            elif key == 78:
                if self.currPage > 1:
                    self.position = 0
                    self.currPage -= 1
            elif key == 71:
                self.position = self.getLastElem() - 1
            else:
                self.command = key

        self.window.erase()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()
