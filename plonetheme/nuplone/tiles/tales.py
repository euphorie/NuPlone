import logging
import re
from chameleon.zpt.expressions import ExpressionTranslator
from chameleon.zpt.interfaces import IExpressionTranslator
from chameleon.core import types
from zope.interface import implements
from plonetheme.nuplone.tiles.tile import getTile
from plonetheme.nuplone.utils import SimpleLiteral

log = logging.getLogger(__name__)


def _lookup_tile(context, request, name):
    tile=getTile(context, request, name)
    if tile is None:
        return u""
    return SimpleLiteral(tile())



class TileTranslator(ExpressionTranslator):
    implements(IExpressionTranslator)

    symbol = "_lookup_tile"
    re_name = re.compile(r"^[a-zA-Z0-9_.-]+$")

    def translate(self, string, escape=None):
        if not string:
            return None
        string=string.strip()
        if self.re_name.match(string) is None:
            raise SyntaxError(string)
        value=types.value("%s(context, request, '%s')" % (self.symbol, string))
        value.symbol_mapping[self.symbol]=_lookup_tile
        return value

