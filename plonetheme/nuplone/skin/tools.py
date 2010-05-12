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
        return utils.viewType(self.context, self.request)

    def formatDate(self, date, length="long"):
        return self.request.locale.dates.getFormatter("date", length).format(date)

    def formatTime(self, time, length=None):
        return self.request.locale.dates.getFormatter("time", length).format(time)

    def formatDatetime(self, timestamp, length="long"):
        return self.request.locale.dates.getFormatter("dateTime", length).format(timestamp)

    def formatDecimal(self, value, length=None):
        return self.request.locale.numbers.getFormatter("decimal", length).format(value)

    def formatPercentage(self, value, length=None):
        return self.request.locale.numbers.getFormatter("percent", length).format(value)

