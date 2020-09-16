from Menu import Menu, MenuItem
from ViewManager import viewManager
from PlaylistMenu import PlaylistMenu

class MainMenuItem(MenuItem):

    def __init__(self, name, component):
        super().__init__(name)
        self.component = component

    def onSelect(self):
        viewManager.setMainView(self.component())


class MainMenu(Menu):

    def __init__(self):
        items = [
            MainMenuItem("Playlists", PlaylistMenu)
        ]
        super().__init__("Main Menu", items)


