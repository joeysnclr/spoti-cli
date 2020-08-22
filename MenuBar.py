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
        self.songInfoScroll = ScrollText("current song", 1)

    def generatePlayBar(self, width):
        timeCurr = utils.msFormat(self.player.currentTime)
        timeTotal = utils.msFormat(self.player.currentTotalTime)
        bar = f"{timeCurr}/{timeTotal} ["
        barWidth = width - len(bar) - 2
        barPercent = self.player.currentTime / self.player.currentTotalTime
        barChars = int(barPercent * barWidth)
        for i in range(barChars):
            bar += u'\u2588'
        for i in range(barWidth - barChars):
            bar += " "
        bar += "]"
        return bar

    def generateOutput(self, width, pageTitle, currPage, pages):
        width = width - 2
        songInfo = f"{self.player.currentSong} {self.player.currentArtist}"
        if songInfo != self.songInfoScroll.text:
            self.songInfoScroll = ScrollText(songInfo, width)
        songInfoCurrent = self.songInfoScroll.scroll(1, width)

        return [pageTitle, songInfoCurrent, self.generatePlayBar(width)]


class ScrollText(object):

    def __init__(self, text, width):
        self.text = text
        self.width = width
        self.displayed = ""
        self.rolloverSpacing = 8
        self.currPosition = 0
        self.lastUpdate = time.time()

    def scroll(self, n, width):
        if time.time() - self.lastUpdate < .5:
            return self.displayed
        self.lastUpdate = time.time()
        self.width = width
        if len(self.text) <= width:
            return self.text
        textWithSpacing = self.text + (" " * self.rolloverSpacing)
        start = self.currPosition
        end = self.currPosition + width
        if end > len(textWithSpacing):
            end = len(textWithSpacing)
            rolloverChars = width - (end - start)
        else:
            rolloverChars = 0

        self.displayed = textWithSpacing[start:end]
        self.displayed += textWithSpacing[:rolloverChars]
        if self.currPosition >= len(textWithSpacing):
            self.currPosition = 0
        else:
            self.currPosition += n
        return self.displayed
