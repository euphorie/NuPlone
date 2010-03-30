import logging
from zope.interface import Interface
from zope.component import queryMultiAdapter
from zope.tales.expressions import StringExpr

log = logging.getLogger(__name__)

class TileExpression(StringExpr):
    def __call__(self, econtext):
        name=super(TileExpression, self).__call__(econtext)
        context=econtext.vars["context"]
        request=econtext.vars["request"]

        tile=queryMultiAdapter((context, request), Interface, name=name)
        if tile is None:
            log.warn("Detected reference to non-existing tile '%s' for context %r",
                     name, context)
            return u""

        return tile()

# Zope 2.12 does not support zcml-registration of expression types.
try:
    from Products.Five.browser import pagetemplatefile
    pagetemplatefile.getEngine().registerType("tile", TileExpression)
except ImportError:
    pass

try:
    from Products.PageTemplates import Expressions
    Expressions.getEngine().registerType("tile", TileExpression)
except ImportError:
    pass

