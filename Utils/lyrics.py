import requests
from bs4 import BeautifulSoup
from Utils.utils import readConfig


def getLyrics(song, artist):
    config = readConfig()
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
        songInfo = json['response']['hits'][0]
    songName = songInfo['result']['title']
    songTitle = songInfo['result']['primary_artist']['name']
    songUrl = songInfo['result']['url']
    page = requests.get(songUrl)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    lyricsByLine = lyrics.split('\n')
    lyricsByLine.insert(0, f'{songName} - {songTitle}')
    return lyricsByLine


# print(getLyrics("Affirmative Action", "Nas"))
