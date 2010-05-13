from plonetheme.nuplone.tiles.tile import AppConfigTile
from plonetheme.nuplone.utils import SimpleLiteral

class AnalyticsTile(AppConfigTile):
    def __call__(self):
        self.account=self.data.get("account", None)
        if not self.account:
            return None

        self.domain=self.data.get("domain", None)
        return SimpleLiteral(self.index())
