import os
import platform
import time
import threading
from Components.Main.ViewManager import viewManager
from Utils.utils import msFormat
from Utils.api import spotifyGetAPI, spotifyPutAPI, spotifyPostAPI
from Components.Templates.Component import Component
from Components.Main.Lyrics import Lyrics
from Components.Main.Log import log

term = viewManager.term


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


class Player(Component):

    def __init__(self, name):
        super().__init__(name)
        self.addShortcut("togglePlay", self.togglePlay)
        self.addShortcut("prevSong", self.prevSong)
        self.addShortcut("nextSong", self.nextSong)
        self.addShortcut("toggleShuffle", self.toggleShuffle)
        self.addShortcut("toggleRepeat", self.toggleRepeat)
        self.addShortcut("showLyrics", self.showLyrics)
        self.addShortcut("decreaseVolume", self.decreaseVolume)
        self.addShortcut("increaseVolume", self.increaseVolume)

        self.isLinux = platform.system() == "Linux"
        self.playing = False
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

    def generatePlayBar(self, width):
        barWidth = width
        barPercent = self.currentTime / self.currentTotalTime
        barChars = int(barPercent * barWidth)
        bar = f"{term.green}"
        for i in range(barChars):
            bar += u'\u2588'
        bar += term.bright_black
        for i in range(barWidth - barChars):
            bar += "\u2588"
        bar += f"{term.normal}"
        return bar

    def generatePlayingSymbolAndColor(self):
        playingInfo = [u"\u25A0", term.red] if not self.playing else [
            u"\u25B6", term.green]
        return playingInfo

    def generatePlayingStatus(self):
        timeCurr = msFormat(self.currentTime)
        timeTotal = msFormat(self.currentTotalTime)
        status = f" {timeCurr}/{timeTotal} "
        return status

    def output(self, lines):
        width = viewManager.term.width

        songInfo = f"{self.currentSong} - {self.currentArtist}"

        playingSymbol = self.generatePlayingSymbolAndColor()
        playingStatus = self.generatePlayingStatus()
        playBar = self.generatePlayBar(width)

        shuffled = "On" if self.shuffle else "Off"
        repeatSymbols = {
            "off": "Off",
            "context": "On",
            "track": "On"
        }
        repeat = self.repeat
        volume = self.volume
        playerSettings = f"{playingSymbol[1]}{playingSymbol[0]} {term.normal}{playingStatus} Shuffle: {shuffled}   Repeat: {repeatSymbols[repeat]}    Volume: {volume}%"

        outputLines = [
            f"{playBar}",
            term.blue + songInfo,
            playerSettings
        ]
        return outputLines

    def getPlayerContext(self):
        while not self.stopThread:
            try:
                context = spotifyGetAPI("/me/player")
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
        log.log("Toggled Play")


    def toggleShuffle(self):
        if self.isLinux:
            newState = "true"
            if self.shuffle:
                newState = "false"
            endpoint = "/me/player/shuffle?state=" + newState
            spotifyPutAPI(endpoint)
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
        log.log("Toggled Shuffle")

    def toggleRepeat(self):
        if self.isLinux:
            newState = "off"
            if self.repeat == "off":
                newState = "context"
            endpoint = "/me/player/repeat?state=" + newState
            spotifyPutAPI(endpoint)
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
        log.log("Toggled Repeat")

    def nextSong(self):
        if self.isLinux:
            self.dbusAction(interface.Next)
        else:
            script = 'tell application "Spotify" to next track'
            self.runOsascript(script)
        log.log("Went to Next Song")

    def prevSong(self):
        if self.isLinux:
            self.dbusAction(interface.Previous)
        else:
            script = 'tell application "Spotify" to previous track'
            self.runOsascript(script)
        log.log("Went to Previous Song")

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
        log.log(f"Played song {songURI} in context {contextURI}")


    def playSong(self, songURI):
        if self.isLinux:
            self.dbusAction(interface.OpenUri, songURI)
        else:
            script = f'tell application "Spotify" to play track "{songURI}"'
            self.runOsascript(script)
        log.log(f"Played song {songURI}")

    def changeVolume(self, amount):
        if self.isLinux:
            newVolume = self.volume + amount
            if newVolume > 100:
                newVolume = 100
            elif newVolume < 0:
                newVolume = 0
            endpoint = "/me/player/volume?volume_percent=" + str(newVolume)
            spotifyPutAPI(endpoint)
        else:
            script = f'tell application "Spotify" to set sound volume to sound volume + {amount}'
            self.runOsascript(script)

    def increaseVolume(self):
        self.changeVolume(10)
        log.log("Increased Volume")

    def decreaseVolume(self):
        self.changeVolume(-10)
        log.log("Decreased Volume")

    def addToQueue(self, songURI):
        endpoint = f"/me/player/queue?uri={songURI}"
        spotifyPostAPI(endpoint, {})
        log.log(f"Added {songURI} to queue")

    def showLyrics(self):
        viewManager.setMainView(Lyrics(self.currentSong, self.currentArtist))


player = Player("player")

# song = "spotify:track:6glsMWIMIxQ4BedzLqGVi4"
# player.addToQueue(song)
# context = "spotify:playlist:6sFCSiF2JWWCGnJ76yw93o"


# p = Player()
# p.playSongInContext(song, context)
# p.playSong(song)
