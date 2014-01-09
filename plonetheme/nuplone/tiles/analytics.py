from AccessControl import getSecurityManager
from plonetheme.nuplone.tiles.tile import AppConfigTile
from plonetheme.nuplone.utils import SimpleLiteral
from plonetheme.nuplone.utils import isAnonymous

_GA_COOKIE = '_nuplone_ga'


def _ga_queue(request):
    cookie = request.cookies.get(_GA_COOKIE, '')
    return filter(None, cookie.split(','))


def trigger_extra_pageview(request, url):
    """Trigger an extra Google Analytics pageview on the next rendered page.
    """
    queue = _ga_queue(request)
    if url not in queue:
        queue.append(url)
    request.response.setCookie(_GA_COOKIE, ','.join(queue), path='/')


class AnalyticsTile(AppConfigTile):
    def _pop_ga_queue(self):
        queue = _ga_queue(self.request)
        self.request.response.expireCookie(_GA_COOKIE, path='/')
        return queue

    def __call__(self):
        self.account = self.data.get("account", None)
        if not self.account:
            return ''
        self.domain = self.data.get("domain", None)
        user = getSecurityManager().getUser()
        self.auth_status = 'anonymous' if isAnonymous(user) else 'authenticated'
        self.ga_queue = self._pop_ga_queue()
        return SimpleLiteral(self.index())
