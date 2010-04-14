import logging
from zope.interface import Interface
from five import grok
from Acquisition import aq_inner
from AccessControl import getSecurityManager
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot

log=logging.getLogger(__name__)

grok.templatedir("templates")


class Login(grok.View):
    grok.context(Interface)
    grok.layer(NuPloneSkin)
    grok.name("login")
    grok.template("login")

    def homeUrl(self, user):
        """Return a suitable `home' for a user if came_from is unset or invalid.
        """
        put=getToolByName(self.context, "portal_url")
        return put.getPortalObject().absolute_url()

    def update(self):
        user=getSecurityManager().getUser()

        if "came_from" in self.request:
            self.came_from=self.request.came_from
        else:
            self.came_from=self.request.environ.get("HTTP_REFERER")
        if self.came_from:
            put=getToolByName(self.context, "portal_url")
            if not put.isURLInPortal(self.came_from):
                self.came_from=None

        self.anonymous=user is None or user.getUserName()=="Anonymous User"
        self.action="%s/@@login" % aq_inner(self.context).absolute_url()

        if not self.anonymous and "login_attempt" in self.request:
            mt=getToolByName(self.context, "portal_membership")
            mt.loginUser(self.request)
            next=self.came_from or self.homeUrl(user)
            self.request.response.redirect(next)

        self.failed=self.anonymous and "login_attempt" in self.request



class Logout(grok.View):
    grok.context(ISiteRoot)
    grok.layer(NuPloneSkin)
    grok.name("logout")

    def render(self):
        mt=getToolByName(self.context, "portal_membership")
        mt.logoutUser(self.request)
        return self.request.response.redirect(aq_inner(self.context).absolute_url())

