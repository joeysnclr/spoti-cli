import Player
import time
import utils


class MenuBar(object):

    def __init__(self):
        self.player = Player.Player()
        self.height = 5
        self.shortcuts = {
            "C": utils.clearCache,
            " ": self.player.togglePlay,
            "H": self.player.prevSong,
            "L": self.player.nextSong,
            "?": self.player.togglePlay
        }

    def generatePlayBar(self, width):
        timeCurr = utils.msFormat(self.player.currentTime)
        timeTotal = utils.msFormat(self.player.currentTotalTime)
        bar = f"{timeCurr}/{timeTotal} ["
        barWidth = width - len(bar) - 2
        barPercent = self.player.currentTime / self.player.currentTotalTime
        barChars = int(barPercent * barWidth)
        for i in range(barChars):
            bar += "█"
        for i in range(barWidth - barChars):
            bar += " "
        bar += "]"

        # barFill = ("\u2588" * barChars) + (" " * (barWidth - barChars))
        return bar

    def generateOutput(self, width, pageTitle, currPage, pages):
        width = width - 2
        return [pageTitle, self.player.currentSong, self.generatePlayBar(width)]
