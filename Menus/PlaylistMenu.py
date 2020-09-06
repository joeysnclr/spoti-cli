import Utils.utils as utils
from MenuComponents.MenuItem import MenuItem
from MenuComponents.Menu import Menu
from Menus.SongMenu import SongMenu


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
                playlist, self.showPlaylist, self.formatPlaylist, self.playlistMatchesSearch)
            menuItems.append(playlistItem)
        self.menu = Menu(menuItems, self.stdscreen, self.title, self.menuBar)
        self.menu.display()

    def showPlaylist(self, playlist):
        songs = self.getSongs(playlist)
        playlistURI = playlist['uri']
        songMenuTitle = playlist['name']
        songMenu = SongMenu(self.stdscreen, self.menuBar,
                            songs, songMenuTitle, playlistURI)
        songMenu.activate()

    def formatPlaylist(self, playlist):
        playlistName = playlist['name']
        playlistSongs = f"{playlist['tracks']['total']} Songs"
        playlistDescription = playlist['description']
        cols = self.stdscreen.getmaxyx()[1] - 2

        column1 = int(cols/5)
        column2 = int(cols/5)
        column3 = int((cols*3) / 5)

        formatted = "{:{}.{}}{:{}.{}}{:>{}}".format(
            playlistName, column1, column1 - 2, playlistSongs, column2, column2 - 2, playlistDescription, column3)
        return formatted

    def playlistMatchesSearch(self, playlist, query):
        return query.lower() in playlist.data['name'].lower()

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
