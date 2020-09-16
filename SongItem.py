from Component import Component
from Menu import MenuItem
from Player import player
from ViewManager import viewManager

term = viewManager.term

class SongItem(MenuItem):

    def __init__(self, songData, contextURI=None):
        super().__init__(songData['track']['name'])
        self.songData = songData
        self.songURI = songData['track']['uri']
        self.contextURI = contextURI

    def onSelect(self):
        if self.contextURI:
            player.playSongInContext(self.songURI, self.contextURI)
        else:
            player.playSong(self.songURI)

    def output(self, lines):
        if self.isActive:
            return term.reverse + self.name + term.normal
        isCurrentSong = player.currentSongURI == self.songURI
        isCurrentContext = player.currentContextURI == self.contextURI
        if isCurrentSong and isCurrentContext:
            return term.green + self.name + term.normal
        return self.name

