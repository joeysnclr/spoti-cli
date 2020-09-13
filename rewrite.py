from ViewManager import viewManager
from Player import player
from Component import Component
from TitleBar import TitleBar
from Menu import Menu
from Menu import MenuItem


items = []
for i in range(100):
    items.append(MenuItem(str(i)))


# initialize components here so that viewManager can init
viewManager.title = TitleBar("title")
viewManager.mainView = Menu("main", items=items)
viewManager.player = player
# start view manager
viewManager.start()
