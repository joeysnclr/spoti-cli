from Components.Templates.Menu import Menu
from Components.Main.SongItem import SongItem
from Utils.api import spotifyGetAPI


class Playlist(Menu):

    def __init__(self, name, playlistId):
        response_items = spotifyGetAPI(
            f"/playlists/{playlistId}/tracks", cache=True, paged=True)
        menu_items = []
        for item in response_items:
            trackName = item['track']['name']
            albumName = item['track']['album']['name']
            albumId = item['track']['album']['id']
            songURI = item['track']['uri']
            duration = item['track']['duration_ms']
            mainArtist = item['track']['artists'][0]['name']
            menu_items.append(SongItem(trackName,mainArtist,albumName,albumId,songURI,duration, f"spotify:playlist:{playlistId}"))
        super().__init__(name, menu_items)
        self.playlistId = playlistId
