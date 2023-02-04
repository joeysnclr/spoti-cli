from Components.Main.ViewManager import viewManager
from Components.Templates.Menu import MenuItem , Menu
from Components.Main.Player import player
from Utils.utils import msFormat
from Utils.api import spotifyGetAPI

term = viewManager.term

class Album(Menu):

    def __init__(self, albumName, albumId):
        response_items = spotifyGetAPI(
            f"/albums/{albumId}/tracks", cache=True, paged=True
        )
        menu_items = []
        for item in response_items:
            trackName = item['name']
            songURI = item['uri']
            duration = item['duration_ms']
            mainArtist = item['artists'][0]['name']
            menu_items.append(SongItem(trackName,mainArtist,albumName,albumId,songURI,duration, f"spotify:album:{albumId}"))
        super().__init__(albumName, menu_items)

class SongItem(MenuItem):

    def __init__(self, trackName, mainArtist, albumName, albumId, songURI, duration, contextURI=None):
        super().__init__(trackName)
        self.addShortcut("addToQueue", self.addToQueue)
        self.addShortcut("goToAlbum", self.goToAlbum)
        self.trackName = trackName
        self.mainArtist = mainArtist
        self.albumName = albumName
        self.albumId = albumId
        self.songURI = songURI
        self.duration = duration
        self.contextURI = contextURI

    def formatSong(self, width):
        time = msFormat(self.duration)
        artistsStr = self.mainArtist
        timeChars = 8
        songChars = int(width * .5)
        artistsChars = int(width * .5) - timeChars

        formatted = "{:{}.{}}{:{}.{}}{:>{}}".format(
            self.trackName, songChars, songChars - 2, artistsStr, artistsChars, artistsChars - 2, time, timeChars)
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

    def goToAlbum(self):
        viewManager.setMainView(Album(self.albumName, self.albumId))