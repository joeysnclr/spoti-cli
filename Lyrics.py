from TextLines import TextLines
import Utils.lyrics as lyrics


class Lyrics(TextLines):

    def __init__(self, song, artist):
        lyricLines = lyrics.getLyrics(song, artist)
        super().__init__("Lyrics", lyricLines)

