from plonetheme.nuplone.tiles.tile import AppConfigTile
from plonetheme.nuplone.utils import SimpleLiteral

class StaticTile(AppConfigTile):
    def __call__(self):
        content=self.data.get("content", None)
        if not content:
            return None
        return SimpleLiteral(content)

