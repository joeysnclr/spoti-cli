from Components.Templates.Menu import Menu
from Components.Main.SongItem import SongItem
from Utils.api import spotifyGetAPI


class LikedSongs(Menu):

    def __init__(self):
        response = spotifyGetAPI(
            f"/me/tracks", cache=True, paged=True)
        items = []
        for track in response:
            items.append(SongItem(track))
        super().__init__("Liked Songs", items)
