import utils
from MenuItem import MenuItem
from Menu import Menu
import lyrics


class LyricsMenu(object):

    def __init__(self, stdscreen, menuBar, song, artist):
        self.stdscreen = stdscreen
        self.menuBar = menuBar
        self.title = "Lyrics: " + song + " - " + artist
        self.song = song
        self.artist = artist
        self.lyrics = lyrics.getLyrics(song, artist)
        self.menu = None

    def activate(self):
        menuItems = []
        for line in self.lyrics:
            lineItem = MenuItem(line, self.selectLine,
                                self.formatLine, self.lineMatchesSearch)
            menuItems.append(lineItem)
        self.menu = Menu(menuItems, self.stdscreen, self.title, self.menuBar)
        self.menu.display()

    def selectLine(self, line):
        return

    def formatLine(self, line):
        return line

    def lineMatchesSearch(self, line, query):
        return query.lower() in line.lower()
