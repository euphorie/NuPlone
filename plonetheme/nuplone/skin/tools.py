from Acquisition import aq_inner
from AccessControl import getSecurityManager
from zope.interface import Interface
from zope.component import queryUtility
from five import grok
from z3c.appconfig.interfaces import IAppConfig
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone import utils
from plonetheme.nuplone import MessageFactory as _

class Tools(grok.View):
    """Basic view to expose utilties to templates."""

    grok.context(Interface)
    grok.name("tools")
    grok.layer(NuPloneSkin)

    # Workaround for grok weirdness: it puts a __getitem__ on a view which
    # assumes there is a template variable
    template = None

    def __init__(self, *a):
        super(Tools, self).__init__(*a)
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

    @utils.reify
    def appConfig(self):
        return queryUtility(IAppConfig) or {}

    def view_type(self):
        return utils.viewType(self.context, self.request)

    @utils.reify
    def site_title(self):
        config=self.appConfig
        title=config.get("site", {}).get("title")
        if title:
            return title
        else:
            return _("default_site_title", default=u"Plone")

    def formatDate(self, date, length="long"):
        return utils.formatDate(self.request, date, length)

    def formatTime(self, time, length=None):
        return utils.formatTime(self.request, time, length)

    def formatDatetime(self, timestamp, length="long"):
        return utils.formatDateTime(self.request, timestamp, length)

    def formatDecimal(self, value, length=None):
        return self.request.locale.numbers.getFormatter("decimal", length).format(value)

    def formatPercentage(self, value, length=None):
        return self.request.locale.numbers.getFormatter("percent", length).format(value)

    def countryName(self, code):
        return self.request.locale.displayNames.territories.get(code.upper())

    def languageName(self, code, default=None):
        code=code.lower()
        names=self.request.locale.displayNames.languages
        return names.get(code, default)

    def checkPermission(self, permission):
        return utils.checkPermission(self.context, permission)

