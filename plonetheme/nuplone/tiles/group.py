from Acquisition import aq_inner
from plonetheme.nuplone.tiles.tile import AppConfigTile
from plonetheme.nuplone.tiles.tile import getTile
from plonetheme.nuplone.utils import viewType
from zExceptions import NotFound

import re


_compiles = {}


class GroupTile(AppConfigTile):
    TILE_EXPR = re.compile(r"(?P<name>\S+)\s*(?:\[(?P<condition>.*)\])?")
    tiles = []

    def update(self):
        self.tiles = []
        self.tag = self.data.get("wrapper", "tal:block")
        tiles = self.data.get("tiles", "").strip().splitlines()
        context = aq_inner(self.context)
        request = self.request
        globals = None
        for tile in tiles:
            result = self.TILE_EXPR.match(tile)
            if not result:
                continue
            condition = result.group("condition")
            if condition:
                compiled = _compiles.get(condition)
                if compiled is None:
                    compiled = _compiles[condition] = compile(
                        condition, "<string>", "eval"
                    )
                if globals is None:
                    globals = dict(
                        context=context,
                        request=request,
                        view_type=viewType(context, request),
                    )
                if not eval(compiled, globals):  # nosec  # TODO: get rid of eval
                    continue
            tile = getTile(context, request, result.group("name"))
            self.tiles.append(tile)

    def __call__(self):
        if isinstance(self.context, NotFound):
            return ""
        self.update()
        if not self.tiles:
            return ""
        result = self.index()
        if not result.strip():
            return ""
        config = self.data
        wrapper = config.get("wrapper")
        if wrapper:
            prefix = ["<%s" % wrapper]
            if config.get("id"):
                prefix.append(' id="%s"' % config["id"])
            if config.get("class"):
                prefix.append(' class="%s"' % config["class"])
            prefix.append(">")
            prefix = "".join(prefix)
            postfix = "</%s>" % wrapper
            result = f"{prefix}{result}{postfix}"
        return result
