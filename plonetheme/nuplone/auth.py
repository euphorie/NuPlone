import urllib
from zope.interface import implements
from App.class_init import default__class_init__ as InitializeClass
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.utils import getNavigationRoot


class LoginChallenger(BasePlugin):
    """Simple login challenger which redirects to the login form.
    This can also be done as a setting on the cookie_auth plugin, but we
    do not do that so other themes can still work.
    """
    meta_type = "NuPlone Login Challenger"
    id = "nuplone-challenger"
    implements(IChallengePlugin)

    def challenge(self, request, response):
        if not NuPloneSkin.providedBy(request):
            return False

        came_from=None
        for url in [ "ACTUAL_URL", "VIRTUAL_URL", "URL" ]:
            came_from=request.get(url)
            if came_from:
                break

        navroot=getNavigationRoot(self)
        if came_from:
            url="%s/@@login?%s" % (navroot.absolute_url(),
                                   urllib.urlencode(dict(came_from=came_from)))
        else:
            url="%s/@@login" % navroot.absolute_url()
        response.redirect(url, lock=True)
        return True


InitializeClass(LoginChallenger)

