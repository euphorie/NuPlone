import logging
from zope.interface import Interface
from five import grok
from Acquisition import aq_inner
from AccessControl import getSecurityManager
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from plonetheme.nuplone import MessageFactory as _
from plonetheme.nuplone.utils import isAnonymous
from Products.statusmessages.interfaces import IStatusMessage


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
        self.came_from = self.request.get('came_from')
        if not self.came_from:
            self.came_from = self.request.environ.get("HTTP_REFERER")
        elif '@@reset-password' in self.came_from:
            self.came_from = None

        if self.came_from:
            if ":" not in self.came_from:
                # Mostly for mechanize/testbrowser which starts with a bogus 'localhost' as referer.
                self.came_from=None
            else:
                put=getToolByName(self.context, "portal_url")
                if not put.isURLInPortal(self.came_from):
                    self.came_from=None

        self.anonymous=isAnonymous(user)
        self.action="%s/@@login" % aq_inner(self.context).absolute_url()

        if not self.anonymous and "login_attempt" in self.request:
            flash=IStatusMessage(self.request).addStatusMessage
            flash(_(u"message_logged_in", default=u"You have been logged in."), "success")
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
        flash=IStatusMessage(self.request).addStatusMessage
        if not isAnonymous():
            mt=getToolByName(self.context, "portal_membership")
            mt.logoutUser(self.request)
            flash(_(u"message_logged_out", default=u"You have been logged out."), "success")
        else:
            flash(_(u"message_already_logged_out", default=u"You were already logged out."), "notice")
        return self.request.response.redirect(aq_inner(self.context).absolute_url())

