from Components.Main.ViewManager import viewManager
from Components.Templates.Menu import Menu, MenuItem
from Components.Main.PlaylistMenu import PlaylistMenu
from Components.Main.LikedSongs import LikedSongs


class MainMenuItem(MenuItem):

    def __init__(self, name, component):
        super().__init__(name)
        self.component = component

    def onSelect(self):
        viewManager.setMainView(self.component())


class MainMenu(Menu):

    def __init__(self):
        items = [
            MainMenuItem("Playlists", PlaylistMenu),
            MainMenuItem("Liked Songs", LikedSongs)
        ]
        super().__init__("Main Menu", items)
