import time
import requests
from Utils.utils import readConfig, writeConfig, readCache, writeCache, endpointIsCached, cacheResponse
from Utils.authenticate import getTokens

def getUserData():
    config = readConfig()
    user = spotifyGetAPI("/me/")
    config['userId'] = user['id']
    writeConfig(config)

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


