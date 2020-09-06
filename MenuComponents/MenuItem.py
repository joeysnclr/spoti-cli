
class MenuItem(object):

    def __init__(self, data, onSelectMethod, formatMethod, matchesSearch, isActive=None):
        self.data = data
        self.onSelectMethod = onSelectMethod
        self.formatMethod = formatMethod
        self.isActive = isActive
        self.matchesSearch = matchesSearch
