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
        barWidth = width - 2
        barPercent = self.player.currentTime / self.player.currentTotalTime
        barChars = int(barPercent * barWidth)
        bar = "["
        for i in range(barChars):
            bar += u'\u2588'
        for i in range(barWidth - barChars):
            bar += " "
        bar += "]"
        return bar

    def generatePlayingSymbolAndColor(self):
        playingInfo = [u"\u25A0", 4] if not self.player.playing else [
            u"\u25B6", 1]
        return playingInfo

    def generatePlayingStatus(self):
        timeCurr = utils.msFormat(self.player.currentTime)
        timeTotal = utils.msFormat(self.player.currentTotalTime)
        status = f" {timeCurr}/{timeTotal} "
        return status

    def generateOutput(self, width, curses):
        width = width - 2

        songInfo = f"{self.player.currentSong} - {self.player.currentArtist}"
        if songInfo != self.songInfoScroll.text:
            self.songInfoScroll = ScrollText(songInfo, width)
        songInfoCurrent = self.songInfoScroll.scroll(2, width)

        playingSymbol = self.generatePlayingSymbolAndColor()
        playingStatus = self.generatePlayingStatus()
        playBar = self.generatePlayBar(width - len(playingStatus))

        shuffled = "On" if self.player.shuffle else "Off"
        repeatSymbols = {
            "off": "Off",
            "context": "On",
            "track": "On"
        }
        repeat = self.player.repeat
        volume = self.player.volume
        playerSettings = f"Shuffle: {shuffled}   Repeat: {repeatSymbols[repeat]}    Volume: {volume}%"

        output = [
            [[songInfoCurrent, 0, curses.color_pair(3)]],
            [
                [playingSymbol[0], 0, curses.color_pair(playingSymbol[1])],
                [playingStatus, 1, curses.A_NORMAL],
                [playBar, len(playingStatus), curses.color_pair(1)]
            ],
            [
                [playerSettings, 0, curses.A_NORMAL]
            ]
        ]
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

        self.displayed = textWithSpacing[start: end]
        self.displayed += textWithSpacing[: rolloverChars]
        if self.currPosition >= len(textWithSpacing):
            self.currPosition = 0
        else:
            self.currPosition += n
        return self.displayed
