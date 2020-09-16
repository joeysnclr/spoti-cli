from ViewManager import viewManager
from Player import player
from Component import Component
from TitleBar import TitleBar
from Menu import Menu, MenuItem
from SongItem import SongItem
from Utils import utils

def startApp():
    items = []
    response = utils.spotifyGetAPI("/playlists/6sFCSiF2JWWCGnJ76yw93o")
    context = response['uri']
    tracks = response["tracks"]["items"]
    for track in tracks:
        x = SongItem(track, contextURI=context)
        items.append(x)

    # initialize components here so that viewManager can init
    viewManager.title = TitleBar("title")
    viewManager.mainView = Menu("main", items=items)
    viewManager.player = player
    viewManager.start()


if __name__ == "__main__":
    # clears cache from last session
    utils.clearCache()

    # gets config
    config = utils.readConfig()


    # spotify user log in if first time
    if not config.get("hasVerified", False):
        utils.verify()
    else:
        utils.getTokens()
    # start view manager
    startApp()
    quit()
