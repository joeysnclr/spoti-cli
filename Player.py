import os
import time
import utils
import threading


class Player():

    def __init__(self):
        self.playing = False
        self.shuffle = False
        self.repeat = "off"
        self.volume = 0
        self.currentSong = None
        self.currentArtist = None
        self.currentAlbum = None
        self.currentTime = 0
        self.currentTotalTime = 1
        self.currentSongURI = None
        self.currentContextURI = None

        # start thread that gets player context
        self.stopThread = False
        threading.Thread(target=self.getPlayerContext, daemon=True).start()

        # set spotify volume to 100 on startup
        self.changeVolume(100)

    def getPlayerContext(self):
        while not self.stopThread:
            try:
                context = utils.spotifyGetAPI("/me/player")
                self.playing = context['is_playing']
                self.shuffle = context['shuffle_state']
                self.repeat = context['repeat_state']
                self.volume = context['device']['volume_percent']
                self.currentTime = context['progress_ms']
                if context['item']:
                    self.currentSong = context['item']['name']
                    self.currentArtist = context['item']['artists'][0]['name']
                    self.currentAlbum = context['item']['album']['name']
                    self.currentTotalTime = context['item']['duration_ms']
                    self.currentSongURI = context['item']['uri']
                if context['context']:
                    self.currentContextURI = context['context']['uri']
                time.sleep(0.1)
            except:
                time.sleep(1)
                continue

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

    def changeVolume(self, amount):
        script = f'tell application "Spotify" to set sound volume to sound volume + {amount}'
        self.runOsascript(script)

    def increaseVolume(self):
        self.changeVolume(10)

    def decreaseVolume(self):
        self.changeVolume(-10)


# song = "spotify:track:6glsMWIMIxQ4BedzLqGVi4"
# context = "spotify:playlist:6sFCSiF2JWWCGnJ76yw93o"


# p = Player()
# p.toggleRepeat()
# while True:
#     print(p.playing, p.currentSong, p.currentArtist, p.currentAlbum, p.currentTime,
#           p.currentTotalTime, p.shuffle, p.repeat)
#     time.sleep(0.5)
