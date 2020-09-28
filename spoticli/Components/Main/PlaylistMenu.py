from Utils.api import spotifyGetAPI
from Components.Main.ViewManager import viewManager
from Components.Templates.Menu import Menu, MenuItem
from Components.Main.Playlist import Playlist

class PlaylistItem(MenuItem):

    def __init__(self, name, playlistId):
        super().__init__(name)
        self.playlistId = playlistId

    def onSelect(self):
        viewManager.setMainView(Playlist(self.name, self.playlistId))



class PlaylistMenu(Menu):

    def __init__(self):
        name = "Playlist Menu"
        items = []
        response = spotifyGetAPI("/me/playlists", cache=True, paged=True)
        for playlist in response:
            items.append(PlaylistItem(playlist['name'], playlist['id']))
        super().__init__(name, items)
