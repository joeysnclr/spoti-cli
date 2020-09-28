from spoticli.Components.Main.ViewManager import viewManager
from spoticli.Components.Main.Player import player
from spoticli.Components.Main.Log import log
from spoticli.Components.Main.TitleBar import TitleBar
from spoticli.Components.Main.MainMenu import MainMenu
from spoticli.Utils.utils import spotifyCache, userdata
from spoticli.Utils.authenticate import verify, getTokens


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
