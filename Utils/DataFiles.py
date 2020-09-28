import json
from pathlib import Path

class DataFile(object):

    def __init__(self, pathStr, defaultContents={}):
        self.path = Path(pathStr)
        # create file
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.write(defaultContents)
        # update contents if new defaut values have been added
        currContents = self.read()
        for key in defaultContents:
            if key not in currContents:
                currContents[key] = defaultContents[key]
        self.write(currContents)

    def read(self):

        # continous retry to read file - sometimes throws error when accessing file from main thread and child thread
        # success = False
        # while not success:
        #     try:
        #         with open(CONFIG_FILE_PATH, "r+") as file:
        #             config = json.load(file)
        #             success = True
        #     except:
        #         continue
        # return config
        with open(self.path, "r+") as file:
            contents = json.load(file)
        return contents


    def write(self, contents):
        with open(self.path, "w+") as file:
            json.dump(contents, file, indent=4)

    def set(self, key, value):
        contents = self.read()
        contents[key] = value
        self.write(contents)

    def get(self, key, default=False):
        contents = self.read()
        if key not in contents:
            return default
        return contents[key]

class CacheFile(DataFile):

    def __init__(self, path, defaultContents={}):
        super().__init__(path, defaultContents)

    def isCached(self, key):
        contents = self.read()
        return key in contents

    def clear(self):
        self.write({})


class ShortcutsFile(DataFile):

    def __init__(self, path, defaultContents={}):
        super().__init__(path, defaultContents)

    def getAction(self, inputKey):
        shortcuts = self.read()
        for action in shortcuts:
            keyData = shortcuts[action]
            if isinstance(keyData, list):
                if inputKey in keyData:
                    return action
            else:
                if inputKey == keyData:
                    return action
        return None

