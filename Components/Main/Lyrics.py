from Components.Templates.TextLines import TextLines
from Utils.lyrics import getLyrics


class Lyrics(TextLines):

    def __init__(self, song, artist):
        lyricLines = getLyrics(song, artist)
        super().__init__("Lyrics", lyricLines)

