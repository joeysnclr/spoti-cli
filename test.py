import curses
from curses import panel


class Menu(object):
    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.active = None
        self.items = items

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def setActive(self, i):
        self.active = i

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.clear()
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL
                activeString = ""
                if self.active == index:
                    activeString = "This one"

                msg = f"{activeString} {item[0]}"
                self.window.addstr(1 + index, 1, msg, mode)

            key = self.window.getch()

            if key in [108, curses.KEY_ENTER, ord("\n")]:
                self.items[self.position][1](self.position)
            elif key == curses.KEY_UP or key == 107:
                self.navigate(-1)
            elif key == curses.KEY_DOWN or key == 106:
                self.navigate(1)
            elif key == 104:
                # exit submenu
                break
            elif key == 113:
                quit()

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()


class PlaylistNav(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)
        self.submenu = None

        main_menu_items = [
            ("playlist1", self.playlistMenu),
            ("playlist2", self.playlistMenu),
            ("playlist3", self.playlistMenu),
        ]
        main_menu = Menu(main_menu_items, self.screen)
        main_menu.display()

    def playlistMenu(self, playlistIndex):
        submenu_items = [
            ("song1", self.playSong),
            ("song2", self.playSong),
            ("song3", self.playSong),
            ("song4", self.playSong),
            ("song5", self.playSong)
        ]
        self.submenu = Menu(submenu_items, self.screen)
        # if song in items is playing, set it as active
        self.submenu.display()

    def playSong(self, songIndex):
        self.submenu.active = songIndex


if __name__ == "__main__":
    curses.wrapper(PlaylistNav)
