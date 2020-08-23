import curses
from curses import panel
import time
import math
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
        # curses.halfdelay(8)  # set frame update in ms
        self.window.nodelay(1)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_WHITE)

        # menu data
        self.title = title
        self.menuBar = menuBar
        self.position = 0
        self.active = None
        self.items = items
        self.currItems = self.items
        self.shortcutMode = "normal"
        self.inputFocused = False
        self.searchQuery = ""
        self.currPage = 1

    def initPaging(self):
        """
        inits paging
        """
        self.winHeight = self.stdscreen.getmaxyx()[0]

        self.perPage = self.winHeight - self.menuBar.height - 2
        self.pages = math.ceil(len(self.currItems) / self.perPage)
        if self.currPage > self.pages or self.currPage < 1:
            self.currPage = 1
            self.position = 0

    def getLastElem(self):
        """
        returns index of last visible element on screen
        """
        first = self.perPage * (self.currPage - 1)
        last = self.perPage * (self.currPage)
        if last > len(self.currItems):
            last = len(self.currItems)
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

    def displayLine(self, y, x, content, color, width):
        if len(content) < width:
            while len(content) < width - 3:
                content += " "
        self.window.addstr(y, x, content, color)

    def getMenuStatus(self):
        if self.inputFocused:
            return f"Search: {self.searchQuery}"
        status = f"Mode: {self.shortcutMode.title()}    {self.title}    Page: {self.currPage}/{self.pages}    Items: {len(self.currItems)}"
        if self.searchQuery:
            status += f"    Search: {self.searchQuery}"
        return status

    def display(self):
        """
        handle frame loop
        """
        self.panel.top()
        self.panel.show()
        self.window.erase()

        while True:
            # if search query is empty when no input is focused go back to normal mode
            if self.searchQuery == "" and not self.inputFocused:
                self.shortcutMode = "normal"
            # filter list items if search mode
            self.currItems = []
            if self.shortcutMode == "search":
                for item in self.items:
                    if item.matchesSearch(item, self.searchQuery):
                        self.currItems.append(item)
            else:
                self.currItems = self.items

            # gather data to be displayed before clearing display
            width = self.stdscreen.getmaxyx()[1]
            self.initPaging()  # responsive paging
            first = self.perPage * (self.currPage - 1)
            last = self.perPage * (self.currPage)
            self.setActive(None)

            shownItems = []
            for index, item in enumerate(self.currItems):
                if index >= first and index < last:
                    formatted = item.formatMethod(item.data)
                    if item.isActive:
                        if item.isActive(item.data):
                            self.setActive(index)
                    shownItems.append((index, item, formatted))

            # set window to override old contents with new contents on next refresh
            self.window.erase()

            menuStatus = self.getMenuStatus()
            menuBar = self.menuBar.generateOutput(
                width, menuStatus)
            i = 0
            for line in menuBar:
                self.displayLine(i, 0, line, curses.A_NORMAL, width)
                i += 1

            for index, item, formatted in shownItems:
                row = index - ((self.currPage - 1) * self.perPage)
                mode = curses.A_NORMAL
                if self.active == index:
                    mode = curses.color_pair(1)
                if row == self.position:
                    if self.active == index:
                        mode = curses.color_pair(2)
                    else:
                        mode = curses.A_REVERSE

                self.displayLine(self.menuBar.height +
                                 row, 0, formatted, mode, width)

            # refreshes the screen
            self.window.refresh()
            curses.doupdate()

            # handles shortcuts
            key = self.window.getch()

            if key != -1:
                # handling input when input focused
                if self.inputFocused:
                    if key == curses.KEY_BACKSPACE:
                        if len(self.searchQuery) > 0:
                            self.searchQuery = self.searchQuery[:-1]
                    elif key == 27:  # ESC
                        self.searchQuery = ""
                        self.inputFocused = False
                    elif key in [curses.KEY_ENTER, ord("\n")]:  # ENTER
                        self.inputFocused = False
                    else:
                        self.searchQuery += chr(key)
                else:
                    # handles menubar/menuitem shortcuts
                    for sc in self.menuBar.shortcuts:
                        if chr(key) == sc:
                            self.menuBar.shortcuts[sc]()
                    menuItemShortcuts = []
                    for i in menuItemShortcuts:
                        pass

                    # handles menu shortcuts
                    if key in [108, curses.KEY_ENTER, ord("\n")]:
                        itemIndex = self.items.index(
                            shownItems[self.position][1])
                        item = self.items[itemIndex]
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
                    elif chr(key) == "/":
                        self.shortcutMode = "search"
                        self.inputFocused = True
                    elif self.shortcutMode == "search" and key == 27:  # leave search mode
                        self.searchQuery = ""
                        self.shortcutMode = "normal"
            time.sleep(1/60)

        self.window.erase()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()
