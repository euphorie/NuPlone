from plone.tiles import Tile

class TabsTile(Tile):
    def update(self):
        self.tabs=[]

    def __call__(self):
        self.update()
        return self.index()
