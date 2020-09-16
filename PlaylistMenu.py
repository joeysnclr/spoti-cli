from Menu import Menu, MenuItem
import Utils.utils as utils
from ViewManager import viewManager
from Playlist import Playlist

class PlaylistItem(MenuItem):

    def __init__(self, name, playlistId):
        super().__init__(name)
        self.playlistId = playlistId

    def onSelect(self):
        viewManager.setMainView(Playlist(self.playlistId))



class PlaylistMenu(Menu):

    def __init__(self):
        name = "Playlist Menu"
        items = []
        response = utils.spotifyGetAPI("/me/playlists", cache=True)
        playlists = response['items']
        for playlist in playlists:
            items.append(PlaylistItem(playlist['name'], playlist['id']))
        super().__init__(name, items)
