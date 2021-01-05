from Products.Five import BrowserView
from plonetheme.nuplone.tiles.tile import getTile


class Layout(BrowserView):

    def get_tile(self, name):
        return getTile(self.context, self.request, name)()
