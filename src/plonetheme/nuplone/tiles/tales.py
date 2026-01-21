from chameleon.utils import Markup
from plonetheme.nuplone import MessageFactory as _
from plonetheme.nuplone.tiles.tile import getTile
from Products.PageTemplates.Expressions import getTrustedEngine
from zope.tales.expressions import StringExpr

import logging


log = logging.getLogger(__name__)


class TileExpression(StringExpr):
    def __call__(self, econtext):
        name = super().__call__(econtext)
        context = econtext.vars["context"]
        request = econtext.vars["request"]

        tile = getTile(context, request, name)
        if tile is None:  # XXX Use custom exception?
            log.warning("Request for unknown tile %s", name)
            return ""

        try:
            return Markup(tile())
        except Exception:
            log.exception("Error rendering tile: %r", name)
            return _(
                "tile_render_error_message",
                mapping={"name": name},
                default="Error rendering tile ${name}",
            )


engine = getTrustedEngine()
engine.registerType("tile", TileExpression)
