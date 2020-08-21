import curses
from curses import panel
import math
import MenuBar


class Menu(object):
    def __init__(self, items, stdscreen, title, menuBar, shortcuts={}):
        # init window stuff
        self.stdscreen = stdscreen
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

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
        self.shortcuts = shortcuts
        self.command = ""
        self.currPage = 1
        self.initPaging()

    def initPaging(self):
        """
        inits paging
        """
        self.winHeight = self.stdscreen.getmaxyx()[0]

        self.perPage = self.winHeight - 5
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

    def display(self):
        """
        handle frame loop
        """
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.clear()
            self.window.refresh()
            curses.doupdate()

            self.initPaging()  # responsive paging

            width = self.stdscreen.getmaxyx()[1]
            menuBar = self.menuBar.generateOutput(
                width, self.title, self.currPage, self.pages)
            menuBarHeight = len(menuBar.split("\n"))

            self.window.addstr(
                1, 0, menuBar, curses.A_NORMAL)
            first = self.perPage * (self.currPage - 1)
            last = self.perPage * (self.currPage)

            for index, item in enumerate(self.items):
                if index >= first and index < last:
                    row = index - ((self.currPage - 1) * self.perPage)
                else:
                    continue

                if row == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                if self.active == index:
                    if self.position == row:
                        mode = curses.color_pair(2)
                    else:
                        mode = curses.color_pair(1)

                msg = f"{item[0]}"
                self.window.addstr(1 + menuBarHeight + row, 0, msg, mode)

            key = self.window.getch()

            for sc in self.shortcuts:
                if key == sc:
                    self.shortcuts[sc]()

            if key in [108, curses.KEY_ENTER, ord("\n")]:
                index = self.position + \
                    (self.perPage * (self.currPage - 1))
                self.items[self.position][1](index)
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

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()
