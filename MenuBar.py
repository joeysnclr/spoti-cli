import Player
import time
import utils


class MenuBar(object):

    def __init__(self):
        self.player = Player.Player()

    def getPlayBar(self, width):
        p = self.player
        fill = "#"
        percent = p.currentTime / p.currentTotalTime
        blocks = round(percent * width)

        current = utils.msFormat(p.currentTime)
        total = utils.msFormat(p.currentTotalTime)

        # playBar = fill * blocks
        playBar = f"{current}\t{total}"
        return playBar

    def generateOutput(self, width, pageTitle, currPage, pages):
        p = self.player
        line1 = self.getPlayBar(width)
        line2 = f"{p.currentSong} {p.currentArtist}"
        line3 = f"{pageTitle} {currPage}/{pages}"
        menuBar = "\n".join([line1, line2, line3])
        return menuBar
