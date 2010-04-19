from Acquisition import aq_inner
from AccessControl import getSecurityManager
from zope.interface import Interface
from five import grok
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone import utils

class Tools(grok.View):
    """Basic view to expose utilties to templates."""

    grok.context(Interface)
    grok.name("tools")
    grok.layer(NuPloneSkin)

    def update(self):
        self.user=getSecurityManager().getUser()
        self.anonymous=self.user is None or self.user.getUserName()=="Anonymous User"
        self.portal=utils.getPortal(self.context)
        self.portal_url=self.portal.absolute_url()
        self.navroot=utils.getNavigationRoot(self.context)
        self.navroot_url=self.navroot.absolute_url()
        self.context_url=aq_inner(self.context).absolute_url()

    def render(self):
        """Little trick to make it easier to access this via from a TALES
        expression."""
        return self

    def view_type(self):
        """Determine what type of view the user is looking at. This returns
        one of three options: ``view`` for normal object views, ``edit``
        for edit forms, and ``other`` for all other types."""
# XXX How to check for add views?

        for url in [ "ACTUAL_URL", "VIRTUAL_URL", "URL" ]:
            current_url=self.request.get(url)
            if current_url is not None:
                break
        else:
            return "view"

        if current_url.endswith("/"):
            current_url=current_url[:-1]

        if current_url.endswith("@@edit"):
            return "edit"

        if current_url==aq_inner(self.context).absolute_url():
            return "view"

        return "other"
