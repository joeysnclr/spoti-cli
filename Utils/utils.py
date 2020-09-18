import webbrowser
import json
import threading
import time
import requests
import os
import sys


CONFIG_DIR_PATH = os.path.abspath(os.path.expanduser("~/.config/terminal-spotify/"))
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, "config.json")

if not os.path.exists(CONFIG_DIR_PATH):
    os.makedirs(CONFIG_DIR_PATH, exist_ok=True)


CACHE_DIR_PATH = os.path.abspath(os.path.expanduser("~/.cache/terminal-spotify/"))
CACHE_FILE_PATH = os.path.join(CACHE_DIR_PATH, "cache.json")

if not os.path.exists(CACHE_DIR_PATH):
    os.makedirs(CACHE_DIR_PATH, exist_ok=True)



def createConfig():
    config = {'hasVerified': False}
    open(CONFIG_FILE_PATH, 'a').close()
    writeConfig(config)


def readConfig():
    if not os.path.exists(CONFIG_FILE_PATH):
        createConfig()
    # continous retry to read file - sometimes throws error when accessing file from main thread and child thread
    success = False
    while not success:
        try:
            with open(CONFIG_FILE_PATH, "r+") as file:
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
            with open(CONFIG_FILE_PATH, "w") as file:
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
    open(CACHE_FILE_PATH, 'a').close()
    writeCache(cache)


def readCache():
    if not os.path.exists(CACHE_FILE_PATH):
        createCache()
    with open(CACHE_FILE_PATH, "r+") as file:
        cache = json.load(file)
    return cache


def clearCache():
    writeCache({})


def writeCache(cache):
    with open(CACHE_FILE_PATH, "w") as file:
        json.dump(cache, file)


def endpointIsCached(endpoint):
    cache = readCache()
    return endpoint in cache


def cacheResponse(endpoint, response):
    cache = readCache()
    cache[endpoint] = response
    writeCache(cache)
