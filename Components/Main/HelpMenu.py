from Components.Templates.TextLines import TextLines
from Utils.utils import shortcuts

class HelpMenu(TextLines):

    def __init__(self):
        super().__init__("Help Menu", self.getShortcutList())

    def getShortcutList(self):
        shortcutData = shortcuts.read()
        longestDesc = 0
        for shortcut in shortcutData:
            if len(shortcut) > longestDesc:
                longestDesc = len(shortcut)
        lines = []
        for shortcut in shortcutData:
            key = shortcutData[shortcut]
            if isinstance(key, list):
                key = ", ".join(key)
            line = "{:{}}   {}".format(shortcut, longestDesc, key)
            lines.append(line)
        return lines





