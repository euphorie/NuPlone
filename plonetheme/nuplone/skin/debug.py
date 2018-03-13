from AccessControl import getSecurityManager
from Acquisition import aq_inner
from five import grok
from zExceptions import Unauthorized
from zope.interface import Interface

import Globals



class WhoAmI(grok.View):
    """Simple view to help debug authorisation problems. This view returns
    the id and login name of the current user and all his roles, both global
    and within the current context.

    This view is only accessible when Zope is running in debug mode.
    """
    grok.context(Interface)
    grok.name("whoami")
    grok.require("zope2.Public")

    def update(self):
        if not Globals.DevelopmentMode:
            raise Unauthorized

    def render(self):
        user = getSecurityManager().getUser()
        output = []
        output.append("User id: %s" % user.getId())
        output.append("Login  : %s" % user.getUserName())
        output.append("Roles  : %s" % " ".join(user.getRoles()))
        output.append(
            "Local R: %s" %
            " ".join(user.getRolesInContext(aq_inner(self.context)))
        )

        self.request.response.setHeader("Content-Type", "text/plain")
        return "\n".join(output)
