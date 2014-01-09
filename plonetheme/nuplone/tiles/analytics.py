from AccessControl import getSecurityManager
from plonetheme.nuplone.tiles.tile import AppConfigTile
from plonetheme.nuplone.utils import SimpleLiteral
from plonetheme.nuplone.utils import isAnonymous


class AnalyticsTile(AppConfigTile):
    def __call__(self):
        self.account = self.data.get("account", None)
        if not self.account:
            return ''
        self.domain = self.data.get("domain", None)
        user = getSecurityManager().getUser()
        self.auth_status = 'anonymous' if isAnonymous(user) else 'authenticated'
        return SimpleLiteral(self.index())
