from Components.Main.ViewManager import viewManager
from Components.Templates.Component import Component
from Components.Templates.Menu import MenuItem
from Components.Main.Player import player
from Utils.utils import msFormat

term = viewManager.term

class SongItem(MenuItem):

    def __init__(self, songData, contextURI=None):
        super().__init__(songData['track']['name'])
        self.addShortcut("addToQueue", self.addToQueue)
        self.songData = songData
        self.songURI = songData['track']['uri']
        self.contextURI = contextURI

    def formatSong(self, width):
        track = self.songData['track']
        songName = track['name']
        dur = track['duration_ms']
        time = msFormat(dur)
        artistsStr = track['artists'][0]['name']
        timeChars = 8
        songChars = int(width * .5)
        artistsChars = int(width * .5) - timeChars

        formatted = "{:{}.{}}{:{}.{}}{:>{}}".format(
            songName, songChars, songChars - 2, artistsStr, artistsChars, artistsChars - 2, time, timeChars)
        return formatted

    def onSelect(self):
        if self.contextURI:
            player.playSongInContext(self.songURI, self.contextURI)
        else:
            player.playSong(self.songURI)

    def output(self, lines):
        width = term.width
        output = self.formatSong(width)
        if self.isActive:
            return term.reverse + output + term.normal
        isCurrentSong = player.currentSongURI == self.songURI
        isCurrentContext = player.currentContextURI == self.contextURI
        if isCurrentSong and isCurrentContext:
            return term.green + output + term.normal
        return output

    def addToQueue(self):
        player.addToQueue(self.songURI)



