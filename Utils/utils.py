import webbrowser
import json
import threading
import Utils.server as server
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


def spotifyGetAPI(endpoint, cache=False):
    if cache:
        if endpointIsCached(endpoint):
            return readCache()[endpoint]

    success = False
    while not success:
        config = readConfig()
        url = "https://api.spotify.com/v1" + endpoint
        headers = {"Authorization": "Bearer " + config["access_token"]}
        try:
            response = requests.get(url, headers=headers)
        except:
            time.sleep(1)
            continue
        if response.status_code == 200 and 'error' not in response.json():
            success = True
        elif response.status_code == 429:
            retryAfter = int(response.headers['Retry-After'])
            time.sleep(retryAfter)
        else:
            getTokens()
    if cache:
        cacheResponse(endpoint, response.json())

    return response.json()


def spotifyPostAPI(url, payload):
    success = False
    while not success:
        try:
            response = requests.post(url, data=payload)
        except:
            time.sleep(1)
            continue
        if response.status_code == 200 and 'error' not in response.json():
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


def getUserData():
    config = readConfig()
    user = spotifyGetAPI("/me/")
    config['userId'] = user['id']
    writeConfig(config)


def getTokens():
    # use code from verification if new user, else use refresh token
    config = readConfig()
    clientId = config['clientId']
    clientSecret = config['clientSecret']
    if 'refresh_token' in config:
        code = config['refresh_token']
        body = {
            "grant_type": "refresh_token",
            "refresh_token": code,
            "client_id": clientId,
            "client_secret": clientSecret
        }
    else:
        code = config['code']
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:5000/auth",
            "client_id": clientId,
            "client_secret": clientSecret
        }

    # send request and save access token and refresh token (if there is one) in config
    postUrl = "https://accounts.spotify.com/api/token"
    response = spotifyPostAPI(postUrl, body)
    accessToken = response['access_token']
    config['access_token'] = accessToken
    if "refresh_token" in response:
        refreshToken = response['refresh_token']
        config['refresh_token'] = refreshToken
    writeConfig(config)


def verify():
    # start server thread
    serverThread = threading.Thread(target=server.run, daemon=True)
    serverThread.start()
    # print instructions
    print("1. Go to the Spotify Dashboard, create an app")
    print("2. Edit settings > add http://localhost:5000/auth as a redirect uri")
    print("3. Enter your Client ID and Client Secret")
    print("4. Login with your Spotify account")
    # get clientId and clientSecret from user, save in config
    clientId = input("Enter your Client ID >> ")
    clientSecret = input("Enter your Client Secret >> ")
    config = readConfig()
    config["clientId"] = clientId
    config["clientSecret"] = clientSecret
    writeConfig(config)
    # set recirectURL, scopes, and generate spotify url
    redirectUri = "http://localhost:5000/auth"
    scopes = "ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing streaming app-remote-control user-read-email user-read-private playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private user-library-modify user-library-read user-top-read user-read-playback-position user-read-recently-played user-follow-read user-follow-modify"
    authURL = f"https://accounts.spotify.com/authorize?client_id={clientId}&response_type=code&redirect_uri={redirectUri}&scope={scopes}"
    # open spotify url in browser
    webbrowser.open(authURL)

    # wait for spotify to redirect user to local server
    # local server will write spotify code to file
    # while loop retrieves code from file once it is there
    # ends server thread when gets code
    codeRecieved = False
    while not codeRecieved:
        currConfig = readConfig()
        if "code" in currConfig:
            code = currConfig["code"]
            codeRecieved = True
            try:
                requests.get("http://localhost:5000/shutdown")
            except:
                pass
        else:
            time.sleep(.5)
    print("recieved code")
    # save code
    config = readConfig()
    config['code'] = code
    writeConfig(config)
    # save that the user has verified
    config = readConfig()
    config['hasVerified'] = True
    writeConfig(config)
    print("verified user")
    # get access/refresh tokens and user info
    getTokens()
    print("retrieved tokens")
    getUserData()
    print("retrieved user data")
