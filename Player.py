import os
import platform
import time
import utils
import threading
if platform.system() == "Linux":
    import dbus
    bus = dbus.SessionBus()
    try:
        proxy = bus.get_object('org.mpris.MediaPlayer2.spotify',
                               '/org/mpris/MediaPlayer2')
        interface = dbus.Interface(
            proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
    except:
        print("make sure spotify is running")
        quit()


class Player():

    def __init__(self):
        self.isLinux = platform.system() == "Linux"

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
        print(script)
        cmd = f"osascript -e '{script}'"
        os.system(cmd)

    def dbusAction(self, function, *args):
        try:
            function(*args)
        except:
            print("make sure spotify is running")

    def togglePlay(self):
        if self.isLinux:
            self.dbusAction(interface.PlayPause)
        else:
            script = 'tell application "Spotify" to playpause'
            self.runOsascript(script)

    def toggleShuffle(self):
        if self.isLinux:
            newState = "true"
            if self.shuffle:
                newState = "false"
            endpoint = "/me/player/shuffle?state=" + newState
            utils.spotifyPutAPI(endpoint)
        else:
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
        if self.isLinux:
            newState = "off"
            if self.repeat == "off":
                newState = "context"
            endpoint = "/me/player/repeat?state=" + newState
            utils.spotifyPutAPI(endpoint)
        else:
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
        if self.isLinux:
            self.dbusAction(interface.Next)
        else:
            script = 'tell application "Spotify" to next track'
            self.runOsascript(script)

    def prevSong(self):
        if self.isLinux:
            self.dbusAction(interface.Previous)
        else:
            script = 'tell application "Spotify" to previous track'
            self.runOsascript(script)

    def playSongInContext(self, songURI, contextURI):
        if self.isLinux:
            # -- cant get dbus to play song in context
            # uri = songURI + "?context=" + contextURI
            # uri = contextURI + ":" + songURI.replace("spotify:", "")
            # uri = songURI + ":" + contextURI
            # uri = songURI + ":" + contextURI.replace("spotify:", "")
            # print(uri)
            # self.dbusAction(interface.OpenUri, uri)
            self.playSong(songURI)
        else:
            script = f'tell application "Spotify" to play track "{songURI}" in context "{contextURI}"'
            self.runOsascript(script)

    def playSong(self, songURI):
        if self.isLinux:
            self.dbusAction(interface.OpenUri, songURI)
        else:
            script = f'tell application "Spotify" to play track "{songURI}"'
            self.runOsascript(script)

    def changeVolume(self, amount):
        if self.isLinux:
            newVolume = self.volume + amount
            if newVolume > 100:
                newVolume = 100
            elif newVolume < 0:
                newVolume = 0
            endpoint = "/me/player/volume?volume_percent=" + str(newVolume)
            utils.spotifyPutAPI(endpoint)
        else:
            script = f'tell application "Spotify" to set sound volume to sound volume + {amount}'
            self.runOsascript(script)

    def increaseVolume(self):
        self.changeVolume(10)

    def decreaseVolume(self):
        self.changeVolume(-10)


song = "spotify:track:6glsMWIMIxQ4BedzLqGVi4"
context = "spotify:playlist:6sFCSiF2JWWCGnJ76yw93o"


p = Player()
p.playSongInContext(song, context)
# p.playSong(song)
