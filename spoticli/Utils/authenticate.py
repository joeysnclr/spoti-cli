import time
import webbrowser
import threading
import requests
from Utils.utils import userdata
from Utils.server import runServer
import Utils.api




def getTokens():
    # use code from verification if new user, else use refresh token
    clientId = userdata.get('clientId')
    clientSecret = userdata.get('clientSecret')
    if 'refresh_token' in userdata.read():
        code = userdata.get('refresh_token')
        body = {
            "grant_type": "refresh_token",
            "refresh_token": code,
            "client_id": clientId,
            "client_secret": clientSecret
        }
    else:
        code = userdata.get('code')
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:5000/auth",
            "client_id": clientId,
            "client_secret": clientSecret
        }

    # send request and save access token and refresh token (if there is one) in config
    postUrl = "https://accounts.spotify.com/api/token"
    response = requests.post(postUrl, data=body).json()
    accessToken = response['access_token']
    userdata.set("access_token", accessToken)
    if "refresh_token" in response:
        refreshToken = response['refresh_token']
        userdata.set("refresh_token", refreshToken)


def verify():
    # start server thread
    serverThread = threading.Thread(target=runServer, daemon=True)
    serverThread.start()
    # print instructions
    print("1. Go to the Spotify Dashboard, create an app")
    print("2. Edit settings > add http://localhost:5000/auth as a redirect uri")
    print("3. Enter your Client ID and Client Secret")
    print("4. Login with your Spotify account")
    # get clientId and clientSecret from user, save in config
    clientId = input("Enter your Client ID >> ")
    clientSecret = input("Enter your Client Secret >> ")
    userdata.set("clientId", clientId)
    userdata.set("clientSecret", clientSecret)
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
        if "code" in userdata.read():
            code = userdata.get("code")
            codeRecieved = True
            try:
                requests.get("http://localhost:5000/shutdown")
            except:
                pass
        else:
            time.sleep(.5)
    print("recieved code")
    # save code
    userdata.set("code", code)
    # save that the user has verified
    userdata.set("hasVerified", True)
    print("verified user")
    # get access/refresh tokens and user info
    getTokens()
    print("retrieved tokens")
    Utils.api.setUserData()
    print("retrieved user data")
