import requests
import utils
from bs4 import BeautifulSoup


def getLyrics(song, artist):
    config = utils.readConfig()
    if 'geniusToken' not in config:
        return ["Could not find Genius API access token"]
    url = 'https://api.genius.com/search'
    headers = {'Authorization': 'Bearer ' + config['geniusToken']}
    data = {'q': song + ' ' + artist}
    response = requests.get(url, data=data, headers=headers)
    json = response.json()
    songInfo = None

    for hit in json['response']['hits']:
        if artist.lower() in hit['result']['primary_artist']['name'].lower():
            songInfo = hit
            break
    if not songInfo:
        return ['Could not find song']
    songUrl = songInfo['result']['url']
    page = requests.get(songUrl)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    return lyrics.split('\n')


# print(getLyrics("Affirmative Action", "Nas"))
