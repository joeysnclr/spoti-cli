import webbrowser
import json
import threading
import time
import requests
import os
import sys


configPath = os.path.abspath(os.path.expanduser("~/.terminal-spotify.json"))
cachePath = os.path.abspath(
    os.path.expanduser("~/.terminal-spotify-cache.json"))


def createConfig():
    config = {'hasVerified': False}
    open(configPath, 'a').close()
    writeConfig(config)


def readConfig():
    if not os.path.exists(configPath):
        createConfig()
    # continous retry to read file - sometimes throws error when accessing file from main thread and child thread
    success = False
    while not success:
        try:
            with open(configPath, "r+") as file:
                config = json.load(file)
                success = True
        except:
            continue
    return config


def writeConfig(config):
    # continous retry to write file - sometimes throws error when accessing file from main thread and child thread
    success = False
    while not success:
        try:
            with open(configPath, "w") as file:
                json.dump(config, file)
                success = True
        except:
            continue


def msFormat(ms):
    minutes = int(ms / 60000)
    seconds = int((ms - (minutes * 60000)) / 1000)
    return f"{minutes}:{seconds:02}"


def createCache():
    cache = {}
    open(cachePath, 'a').close()
    writeCache(cache)


def readCache():
    if not os.path.exists(cachePath):
        createCache()
    with open(cachePath, "r+") as file:
        cache = json.load(file)
    return cache


def clearCache():
    writeCache({})


def writeCache(cache):
    with open(cachePath, "w") as file:
        json.dump(cache, file)


def endpointIsCached(endpoint):
    cache = readCache()
    return endpoint in cache


def cacheResponse(endpoint, response):
    cache = readCache()
    cache[endpoint] = response
    writeCache(cache)
