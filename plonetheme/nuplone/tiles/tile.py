import logging
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts
from zope.component import getUtility
from zope.component import queryMultiAdapter
from plone.tiles.interfaces import ITileDataManager
from plone.tiles.interfaces import ITile
from plone.tiles.tile import Tile
from z3c.appconfig.interfaces import IAppConfig

log = logging.getLogger(__name__)

class IAppConfigTile(ITile):
    """A tile with its configured stored in the application config."""


class AppConfigTile(Tile):
    implements(IAppConfigTile)


class AppConfigTileDataManager(object):
    implements(ITileDataManager)
    adapts(IAppConfigTile)

    def __init__(self, tile):
        self.tile=tile

    def get(self):
        appconfig=getUtility(IAppConfig)
        return appconfig.get("tile:%s" % self.tile.id, {})

    def set(self, data):
        raise NotImplementedError


def getTile(context, request, name):
    appconfig=getUtility(IAppConfig)
    config=appconfig.get("tile:%s" % name, {})
    type=config.get("type", name)
    tile=queryMultiAdapter((context, request), Interface, name=type)
    if tile is None:
        log.warn("Detected reference to non-existing tile '%s' for context %r",
                 name, context)
        return None

    if IAppConfigTile.providedBy(tile):
        tile.id=name

    return tile


