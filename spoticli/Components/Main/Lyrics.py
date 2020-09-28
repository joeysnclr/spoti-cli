from spoticli.Components.Templates.TextLines import TextLines
from spoticli.Utils.lyrics import getLyrics


class Lyrics(TextLines):

    def __init__(self, song, artist):
        lyricLines = getLyrics(song, artist)
        super().__init__("Lyrics", lyricLines)

