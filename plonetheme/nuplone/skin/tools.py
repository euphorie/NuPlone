# coding=utf-8
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from plone import api
from plone.memoize.view import memoize
from plonetheme.nuplone import utils
from Products.Five import BrowserView


class Tools(BrowserView):
    """Basic view to expose utilties to templates."""

    @property
    @memoize
    def user(self):
        return getSecurityManager().getUser()

    @property
    @memoize
    def anonymous(self):
        return self.user is None or self.user.getUserName() == "Anonymous User"

    @property
    @memoize
    def portal(self):
        return utils.getPortal(self.context)

    @property
    @memoize
    def portal_url(self):
        return self.portal.absolute_url()

    @property
    @memoize
    def navroot(self):
        return utils.getNavigationRoot(self.context)

    @property
    @memoize
    def navroot_url(self):
        return self.navroot.absolute_url()

    @property
    @memoize
    def context_url(self):
        return aq_inner(self.context).absolute_url()

    def render(self):
        """Little trick to make it easier to access this via from a TALES
        expression."""
        return self

    def view_type(self):
        return utils.viewType(self.context, self.request)

    def site_title(self):
        return api.portal.get_registry_record("plone.site_title")

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
        code = code.lower()
        names = self.request.locale.displayNames.languages
        return names.get(code, default)

    def checkPermission(self, permission):
        return utils.checkPermission(self.context, permission)
