
class MenuItem(object):

    def __init__(self, data, onSelectMethod, formatMethod, isActive=None):
        self.data = data
        self.onSelectMethod = onSelectMethod
        self.formatMethod = formatMethod
        self.isActive = isActive
