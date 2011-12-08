import logging
from chameleon.tales import StringExpr
from chameleon.astutil import Symbol
from chameleon.astutil import Static
from chameleon.codegen import template
from zope.contentprovider.interfaces import ContentProviderLookupError
from plonetheme.nuplone.tiles.tile import getTile
from plonetheme.nuplone.utils import SimpleLiteral


log = logging.getLogger(__name__)


class TileProviderTraverser(object):
    def __call__(self, context, request, name):
        tile = getTile(context, request, name)
        if tile is None:  # XXX Use custom exception?
            log.warn('Request for unknown tile %s', name)
            return u''
        return SimpleLiteral(tile())


class TileExpression(StringExpr):
    render_tile = Static(
            template("cls()", cls=Symbol(TileProviderTraverser), mode='eval'))

    def __call__(self, target, engine):
        assignment = super(TileExpression, self).__call__(target, engine)
        return assignment + template(
                'target = render_tile(context, request, target.strip())',
                target=target,
                render_tile=self.render_tile)


import five.pt.engine
five.pt.engine.Program.secure_expression_types['tile'] = TileExpression
five.pt.engine.Program.expression_types['tile'] = TileExpression
