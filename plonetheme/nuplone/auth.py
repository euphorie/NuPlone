from zope.interface import implements
from App.class_init import default__class_init__ as InitializeClass
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
from plonetheme.nuplone.skin.interfaces import NuPloneSkin


class LoginChallenger(BasePlugin):
    """Simple login challenger which does nothing, allowing the
    Unauthorized exception view to be used instead.
    """
    meta_type = "NuPlone Login Challenger"
    id = "nuplone-challenger"
    implements(IChallengePlugin)

    def challenge(self, request, response):
        if not NuPloneSkin.providedBy(request):
            return False

        response.setStatus(403)
        response._locked_status = True
        return True


InitializeClass(LoginChallenger)

