import logging
import re
from zope.interface import Interface
from zope.component import queryMultiAdapter
from chameleon.zpt.expressions import ExpressionTranslator
from chameleon.zpt.interfaces import IExpressionTranslator
from chameleon.core import types
from zope.interface import implements

log = logging.getLogger(__name__)


class SimpleLiteral(unicode):
    def __html__(self):
        return unicode(self)

def _lookup_tile(context, request, name):
    tile=queryMultiAdapter((context, request), Interface, name=name)
    if tile is None:
        log.warn("Detected reference to non-existing tile '%s' for context %r",
                 name, context)
        return u""

    return SimpleLiteral(tile())

class TileTranslator(ExpressionTranslator):
    implements(IExpressionTranslator)

    symbol = "_lookup_tile"
    re_name = re.compile(r"^[a-z]+$")

    def translate(self, string, escape=None):
        if not string:
            return None
        string=string.strip()
        if self.re_name.match(string) is None:
            raise SyntaxError(string)
        value=types.value("%s(context, request, '%s')" % (self.symbol, string))
        value.symbol_mapping[self.symbol]=_lookup_tile
        return value

