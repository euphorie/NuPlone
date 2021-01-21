from App.class_init import default__class_init__ as InitializeClass
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from zope.interface import implementer


@implementer(IChallengePlugin)
class LoginChallenger(BasePlugin):
    """Simple login challenger which does nothing, allowing the
    Unauthorized exception view to be used instead.
    """

    meta_type = "NuPlone Login Challenger"
    id = "nuplone-challenger"

    def challenge(self, request, response):
        if not NuPloneSkin.providedBy(request):
            return False

        response.setStatus(403)
        response._locked_status = True
        return True


InitializeClass(LoginChallenger)
