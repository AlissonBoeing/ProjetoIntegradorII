class Treasure:

    def __init__(self, posx, posy, id):
        self.posx = posx
        self.posy = posy
        self.id = id

    def getId(self):
        return self.id

    def getPosx(self):
        return self.posx

    def getPosy(self):
        return self.posy
