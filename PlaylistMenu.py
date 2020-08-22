import utils
from MenuItem import MenuItem
from Menu import Menu


class PlaylistMenu(object):

    def __init__(self, stdscreen, menuBar):
        self.stdscreen = stdscreen
        self.menuBar = menuBar
        self.title = "Your Playlists"
        self.playlists = self.getPlaylists()
        self.menu = None

    def activate(self):
        menuItems = []
        for playlist in self.playlists:
            playlistItem = MenuItem(
                playlist, self.showPlaylist, self.formatPlaylist)
            menuItems.append(playlistItem)
        self.menu = Menu(menuItems, self.stdscreen, self.title, self.menuBar)
        self.menu.display()

    def showPlaylist(self, playlist):
        songs = self.getSongs(playlist)
        playlistName = playlist['name']
        playlistURI = playlist['uri']
        songMenu = SongMenu(self.stdscreen, self.menuBar,
                            songs, playlistName, playlistURI)
        songMenu.activate()

    def formatPlaylist(self, playlist):
        return playlist['name']

    def getSongs(self, playlist):
        playlistId = playlist['id']
        songs = utils.spotifyGetAPI(
            f"/playlists/{playlistId}/tracks", cache=True)['items']
        return songs

    def getPlaylists(self):
        user_id = utils.readConfig()['userId']
        playlistsEndpoint = f"/users/{user_id}/playlists"
        playlists = utils.spotifyGetAPI(playlistsEndpoint, cache=True)['items']
        return playlists


class SongMenu(object):

    def __init__(self, stdscreen, menuBar, songs, title, contextURI=None):
        self.stdscreen = stdscreen
        self.menuBar = menuBar
        self.title = title
        self.songs = songs
        self.contextURI = contextURI
        self.menu = None

    def activate(self):
        menuItems = []
        for song in self.songs:
            songItem = MenuItem(song, self.playSong,
                                self.formatSong, self.isActive)
            menuItems.append(songItem)
        self.menu = Menu(menuItems, self.stdscreen, self.title, self.menuBar)
        self.menu.display()

    def playSong(self, song):
        songId = song['track']['id']
        songURI = f"spotify:track:{songId}"
        if self.contextURI:
            self.menuBar.player.playSongInContext(songURI, self.contextURI)
        else:
            self.menuBar.player.playSong(songURI)

    def formatSong(self, song):
        track = song['track']
        songName = track['name']
        dur = track['duration_ms']
        time = utils.msFormat(dur)
        artistsStr = track['artists'][0]['name']
        cols = self.stdscreen.getmaxyx()[1] - 2
        timeChars = 8
        songChars = int(cols * .5)
        artistsChars = int(cols * .5) - timeChars

        formatted = "{:{}.{}}{:{}.{}}{:>{}}".format(
            songName, songChars, songChars - 2, artistsStr, artistsChars, artistsChars - 2, time, timeChars)
        return formatted

    def isActive(self, song):
        songId = song['track']['id']
        songURI = f"spotify:track:{songId}"
        player = self.menuBar.player
        isCurrentSong = songURI == player.currentSongURI
        isCurrentContext = self.contextURI == player.currentContextURI
        return isCurrentSong and isCurrentContext
