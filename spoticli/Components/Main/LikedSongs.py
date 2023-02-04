from Components.Templates.Menu import Menu
from Components.Main.SongItem import SongItem
from Utils.api import spotifyGetAPI


class LikedSongs(Menu):

    def __init__(self):
        response_items = spotifyGetAPI(
            f"/me/tracks", cache=True, paged=True)
        menu_items = []
        for item in response_items:
            trackName = item['track']['name']
            albumId = item['track']['album']['id']
            albumName = item['track']['album']['name']
            songURI = item['track']['uri']
            duration = item['track']['duration_ms']
            mainArtist = item['track']['artists'][0]['name']
            menu_items.append(SongItem(trackName,mainArtist,albumName,albumId,songURI,duration))
        super().__init__("Liked Songs", menu_items)
