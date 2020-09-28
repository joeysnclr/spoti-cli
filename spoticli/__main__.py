from Components.Main.ViewManager import viewManager
from Components.Main.Player import player
from Components.Main.Log import log
from Components.Main.TitleBar import TitleBar
from Components.Main.MainMenu import MainMenu
from Utils.utils import spotifyCache, userdata
from Utils.authenticate import verify, getTokens


def startApp():
    # initialize components here so that viewManager can init
    viewManager.title = TitleBar("title")
    viewManager.setMainView(MainMenu())
    viewManager.player = player
    viewManager.logOutput = log
    viewManager.start()

def main():
    # clears cache from last session
    spotifyCache.clear()

    # spotify user log in if first time
    if not userdata.get("hasVerified", False):
        verify()
    else:
        getTokens()
    # start view manager
    startApp()
    quit()

if __name__ == "__main__":
    main()
