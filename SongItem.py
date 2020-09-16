from Component import Component
from Menu import MenuItem
from Player import player

class SongItem(MenuItem):

    def __init__(self, songData, contextURI=None):
        super().__init__(songData['track']['name'])
        self.songData = songData
        self.contextURI = contextURI

    def onSelect(self):
        songURI = self.songData['track']['uri']
        if self.contextURI:
            player.playSongInContext(songURI, self.contextURI)
        else:
            player.playSong(songURI)

