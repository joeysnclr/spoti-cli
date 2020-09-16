from ViewManager import viewManager
from Player import player
from Component import Component
from TitleBar import TitleBar
from PlaylistMenu import PlaylistMenu
from SongItem import SongItem
from Utils import utils

def startApp():
    # initialize components here so that viewManager can init
    viewManager.title = TitleBar("title")
    viewManager.setMainView(PlaylistMenu())
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
