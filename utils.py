import webbrowser
import json
import threading
import server
import time
import requests
import os
import sys


def readConfig():
    with open("./clify.json", "r+") as file:
        config = json.load(file)
    return config


def writeConfig(config):
    with open("./clify.json", "w+") as file:
        json.dump(config, file)


def msFormat(ms):
    minutes = int(ms / 60000)
    seconds = int((ms - (minutes * 60000)) / 1000)
    return f"{minutes}:{seconds:02}"


def spotifyGetAPI(endpoint):
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
    return response.json()


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

    postUrl = "https://accounts.spotify.com/api/token"
    # send request and save access token and refresh token (if there is one) in config
    r = requests.post(postUrl, data=body)
    response = r.json()
    accessToken = response['access_token']
    config['access_token'] = accessToken
    if "refresh_token" in response:
        refreshToken = response['refresh_token']
        config['refresh_token'] = refreshToken
    writeConfig(config)


def verify():
    # start server thread
    serverThread = threading.Thread(target=server.run)
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
