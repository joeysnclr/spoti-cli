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


def spotifyGetAPI(endpoint, cache=False, paged=False):
    if cache:
        if endpointIsCached(endpoint):
            return readCache()[endpoint]

    url = "https://api.spotify.com/v1" + endpoint
    output = []
    success = False
    while not success:
        config = readConfig()
        headers = {"Authorization": "Bearer " + config["access_token"]}
        try:
            response = requests.get(url, headers=headers)
        except:
            time.sleep(1)
            continue
        if response.status_code == 200 and 'error' not in response.json():
            if paged:
                content = response.json()
                # append items to response
                for item in content['items']:
                    output.append(item)
                if not content["next"]:
                    success = True
                else:
                    url = content["next"]
            else:
                output = response.json()
                success = True
        elif response.status_code == 429:
            retryAfter = int(response.headers['Retry-After'])
            time.sleep(retryAfter)
        else:
            getTokens()
    if cache:
        cacheResponse(endpoint, output)

    return output


def spotifyPostAPI(endpoint, payload):
    success = False
    while not success:
        config = readConfig()
        url = "https://api.spotify.com/v1" + endpoint
        headers = {"Authorization": "Bearer " + config["access_token"]}
        try:
            response = requests.post(url, data=payload, headers=headers)
        except Exception as e:
            time.sleep(1)
            continue
        if response.status_code == 204:
            return
        elif response.status_code == 200 and 'error' not in response.json():
            success = True
        elif response.status_code == 429:
            retryAfter = int(response.headers['Retry-After'])
            time.sleep(retryAfter)
    return response.json()


def spotifyPutAPI(endpoint):
    success = False
    while not success:
        config = readConfig()
        url = "https://api.spotify.com/v1" + endpoint
        headers = {"Authorization": "Bearer " + config["access_token"]}
        try:
            response = requests.put(url, headers=headers)
        except Exception as e:
            raise Exception(e)
            print(e)
            time.sleep(1)
            continue
        if response.status_code == 204:
            success = True
        elif response.status_code == 429:
            retryAfter = int(response.headers['Retry-After'])
            time.sleep(retryAfter)


