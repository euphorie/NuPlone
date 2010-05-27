import re
from Acquisition import aq_inner
from plonetheme.nuplone.tiles.tile import AppConfigTile
from plonetheme.nuplone.tiles.tile import getTile
from plonetheme.nuplone.utils import viewType

_compiles = {}

class GroupTile(AppConfigTile):
    TILE_EXPR = re.compile("(?P<name>\S+)\s*(?:\[(?P<condition>.*)\])?")
    tiles = []

    def update(self):
        self.tiles=[]
        self.tag=self.data.get("wrapper", "tal:block")
        tiles=self.data.get("tiles", "").strip().splitlines()
        context=aq_inner(self.context)
        request=self.request
        globals=None
        for tile in tiles:
            result=self.TILE_EXPR.match(tile)
            if not result:
                continue
            condition=result.group("condition")
            if condition:
                compiled=_compiles.get(condition)
                if compiled is None:
                    compiled=_compiles[condition]=compile(condition, "<string>", "eval")
                if globals is None:
                    globals=dict(context=context, request=request, view_type=viewType(context, request))
                if not eval(compiled, globals):
                    continue
            tile=getTile(context, request, result.group("name"))
            self.tiles.append(tile)


    def __call__(self):
        self.update()
        if not self.tiles:
            return u""
        result=self.index()
        if not result.strip():
            return u""
        config=self.data
        wrapper=config.get("wrapper")
        if wrapper:
            prefix=[u"<%s" % wrapper]
            if config.get("id"):
                prefix.append(u' id="%s"' % config["id"])
            if config.get("class"):
                prefix.append(u' class="%s"' % config["class"])
            prefix.append(u">")
            prefix=u"".join(prefix)
            postfix=u"</%s>" % wrapper
            result=u"%s%s%s" % (prefix, result, postfix)
        return result

