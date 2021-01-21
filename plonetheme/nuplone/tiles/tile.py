from plone import api
from plone.tiles.interfaces import ITile
from plone.tiles.interfaces import ITileDataManager
from plone.tiles.tile import Tile
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface

import json
import logging


log = logging.getLogger(__name__)


class IAppConfigTile(ITile):
    """A tile with its configured stored in the application config."""


@implementer(IAppConfigTile)
class AppConfigTile(Tile):
    pass


@implementer(ITileDataManager)
@adapter(IAppConfigTile)
class AppConfigTileDataManager(object):
    def __init__(self, tile):
        self.tile = tile

    def get(self):
        try:
            return json.loads(
                api.portal.get_registry_record(
                    "plonetheme.nuplone.appconfigtile_{}".format(self.tile.id),
                    default="{}",
                )
            )
        except Exception:
            log.exception("Cannot get configuration for %r", self.tile.id)
            return {}

    def set(self, data):
        raise NotImplementedError


def getTile(context, request, name):
    config = json.loads(
        api.portal.get_registry_record(
            "plonetheme.nuplone.appconfigtile_{}".format(name), default="{}"
        )
        or "{}"
    )
    type = config.get("type", name)
    tile = queryMultiAdapter((context, request), Interface, name=type)
    if tile is None:
        log.warning(
            "Detected reference to non-existing tile '%s' for context %r", name, context
        )
        return None

    if IAppConfigTile.providedBy(tile):
        tile.id = name

    return tile
