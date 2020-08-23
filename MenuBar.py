import Player
import time
import utils
from LyricsMenu import LyricsMenu


class MenuBar(object):

    def __init__(self, stdscreen):
        self.stdscreen = stdscreen
        self.player = Player.Player()
        self.height = 6
        self.shortcuts = {
            "C": utils.clearCache,
            " ": self.player.togglePlay,
            "H": self.player.prevSong,
            "L": self.player.nextSong,
            "?": self.player.togglePlay,
            "s": self.player.toggleShuffle,
            "r": self.player.toggleRepeat,
            "i": self.showLyrics
            # "=": self.player.increaseVolume,
            # "-": self.player.decreaseVolume
        }
        self.songInfoScroll = ScrollText("current song", 1)

    def showLyrics(self):
        lyricsMenu = LyricsMenu(
            self.stdscreen, self, self.player.currentSong, self.player.currentArtist)
        lyricsMenu.activate()

    def generatePlayBar(self, width):
        timeCurr = utils.msFormat(self.player.currentTime)
        timeTotal = utils.msFormat(self.player.currentTotalTime)
        playingText = u"\u25A0" if self.player.playing else u"\u25B6"
        bar = f"{playingText} {timeCurr}/{timeTotal} ["
        barWidth = width - len(bar) - 2
        barPercent = self.player.currentTime / self.player.currentTotalTime
        barChars = int(barPercent * barWidth)
        for i in range(barChars):
            bar += u'\u2588'
        for i in range(barWidth - barChars):
            bar += " "
        bar += "]"
        return bar

    def generateOutput(self, width, menuStatus):
        width = width - 2

        songInfo = f"{self.player.currentSong} - {self.player.currentArtist}"
        if songInfo != self.songInfoScroll.text:
            self.songInfoScroll = ScrollText(songInfo, width)
        songInfoCurrent = self.songInfoScroll.scroll(2, width)

        playBar = self.generatePlayBar(width)

        shuffled = "On" if self.player.shuffle else "Off"
        repeatSymbols = {
            "off": "Off",
            "context": "On",
            "track": "On"
        }
        repeat = self.player.repeat
        volume = self.player.volume
        playerSettings = f"Shuffle: {shuffled}   Repeat: {repeatSymbols[repeat]}    Volume: {volume}%"

        output = [songInfoCurrent, playBar,
                  playerSettings, "", menuStatus]
        return output


class ScrollText(object):

    def __init__(self, text, width):
        self.text = text
        self.width = width
        self.displayed = ""
        self.rolloverSpacing = 8
        self.currPosition = 0
        self.lastUpdate = -99
        self.updateEvery = .5

    def scroll(self, n, width):
        if time.time() - self.lastUpdate < self.updateEvery:
            return self.displayed
        self.lastUpdate = time.time()
        self.width = width
        if len(self.text) <= width:
            self.displayed = self.text
            return self.displayed
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
