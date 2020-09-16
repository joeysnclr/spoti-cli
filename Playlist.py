from Menu import Menu, MenuItem
from SongItem import SongItem
import Utils.utils as utils

class Playlist(Menu):

    def __init__(self, name, playlistId):
        response = utils.spotifyGetAPI(f"/playlists/{playlistId}/tracks", cache=True, paged=True)
        items = []
        for track in response:
            items.append(SongItem(track, f"spotify:playlist:{playlistId}"))
        super().__init__(name, items)
        self.playlistId = playlistId
