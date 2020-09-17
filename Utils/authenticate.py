import requests
from Utils.utils import readConfig, writeConfig
from Utils.server import runServer




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
    response = requests.post(postUrl, data=body).json()
    accessToken = response['access_token']
    config['access_token'] = accessToken
    if "refresh_token" in response:
        refreshToken = response['refresh_token']
        config['refresh_token'] = refreshToken
    writeConfig(config)


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
