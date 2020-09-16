from Menu import Menu, MenuItem
from SongItem import SongItem
import Utils.utils as utils

class Playlist(Menu):

    def __init__(self, playlistId):
        response = utils.spotifyGetAPI(f"/playlists/{playlistId}", cache=True)
        name = response['name']
        items = []
        for track in response['tracks']['items']:
            items.append(SongItem(track, response['uri']))
        super().__init__(name, items)
        self.playlistId = playlistId
