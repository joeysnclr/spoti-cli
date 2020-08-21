import os
import time
import utils
import threading


class Player():

    def __init__(self):
        self.playing = False
        self.shuffle = None
        self.repeat = None
        self.currentSong = None
        self.currentArtist = None
        self.currentAlbum = None
        self.currentTime = 0
        self.currentTotalTime = 1

        # start thread that gets player context
        self.stopThread = False
        threading.Thread(target=self.getPlayerContext).start()

    def getPlayerContext(self):
        while not self.stopThread:
            context = utils.spotifyGetAPI("/me/player")
            self.playing = context['is_playing']
            self.shuffle = context['shuffle_state']
            self.repeat = context['repeat_state']
            self.currentTime = context['progress_ms']
            if context['item']:
                self.currentSong = context['item']['name']
                self.currentArtist = context['item']['artists'][0]['name']
                self.currentAlbum = context['item']['album']['name']
                self.currentTotalTime = context['item']['duration_ms']
            time.sleep(0.1)

    def runOsascript(self, script):
        cmd = f"osascript -e '{script}'"
        os.system(cmd)

    def togglePlay(self):
        script = 'tell application "Spotify" to playpause'
        self.runOsascript(script)

    def toggleShuffle(self):
        script = '''
            tell application "Spotify"
                if shuffling then
                    set shuffling to false
                else
                    set shuffling to true
                end if
            end tell
        '''
        self.runOsascript(script)

    def toggleRepeat(self):
        script = '''
            tell application "Spotify"
                if repeating then
                    set repeating to false
                else
                    set repeating to true
                end if
            end tell
        '''
        self.runOsascript(script)

    def nextSong(self):
        script = 'tell application "Spotify" to next track'
        self.runOsascript(script)

    def prevSong(self):
        script = 'tell application "Spotify" to previous track'
        self.runOsascript(script)

    def playSongInContext(self, songURI, contextURI):
        script = f'tell application "Spotify" to play track "{songURI}" in context "{contextURI}"'
        self.runOsascript(script)

    def playSong(self, songURI):
        script = f'tell application "Spotify" to play track "{songURI}"'
        self.runOsascript(script)


# song = "spotify:track:6glsMWIMIxQ4BedzLqGVi4"
# context = "spotify:playlist:6sFCSiF2JWWCGnJ76yw93o"


# p = Player()
# p.toggleRepeat()
# while True:
#     print(p.playing, p.currentSong, p.currentArtist, p.currentAlbum, p.currentTime,
#           p.currentTotalTime, p.shuffle, p.repeat)
#     time.sleep(0.5)
