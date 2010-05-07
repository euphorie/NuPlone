from plone.tiles import Tile
from Products.statusmessages.interfaces import IStatusMessage

class StatusmessagesTile(Tile):
    mapping = dict(info="notice",
                   warn="warning")

    def update(self):
        messages=IStatusMessage(self.request).show()
        for message in messages:
            message.type=self.mapping.get(message.type, message.type)
        self.messages=messages

    def __call__(self):
        self.update()
        return self.index()
