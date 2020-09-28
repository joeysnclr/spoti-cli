import webbrowser
import json
import threading
import time
import requests
import os
import sys
from spoticli.Utils.DataFiles import DataFile, CacheFile, ShortcutsFile
from spoticli.Utils.settings import defaultSettings
from spoticli.Utils.shortcuts import defaultShortcuts


USERDATA_PATH = os.path.abspath(os.path.expanduser("~/.config/spoti-cli/userdata.json"))
SETTINGS_PATH = os.path.abspath(os.path.expanduser("~/.config/spoti-cli/settings.json"))
SHORTCUTS_PATH = os.path.abspath(os.path.expanduser("~/.config/spoti-cli/shortcuts.json"))
SPOTIFY_CACHE_PATH = os.path.abspath(os.path.expanduser("~/.cache/spoti-cli/spotify.json"))
GENIUS_CACHE_PATH = os.path.abspath(os.path.expanduser("~/.cache/spoti-cli/genius.json"))


userdata = DataFile(USERDATA_PATH)
settings = DataFile(SETTINGS_PATH, defaultSettings)
shortcuts = ShortcutsFile(SHORTCUTS_PATH, defaultShortcuts)
spotifyCache = CacheFile(SPOTIFY_CACHE_PATH)
geniusCache = CacheFile(GENIUS_CACHE_PATH)


def msFormat(ms):
    minutes = int(ms / 60000)
    seconds = int((ms - (minutes * 60000)) / 1000)
    return f"{minutes}:{seconds:02}"

