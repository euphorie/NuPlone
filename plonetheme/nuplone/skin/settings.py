from AccessControl import getSecurityManager
from five import grok
from zope import schema
from zope.globalrequest import getRequest
from zope.schema.interfaces import IField
from zope.schema.interfaces import IPassword
from plone.directives import form
from plonetheme.nuplone import MessageFactory as _
from z3c.form.interfaces import IDataManager
from z3c.form.interfaces import NO_VALUE
from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

class ISettings(form.Schema):
    fullname = schema.TextLine(
            title=_("label_fullname", default=u"Full name"),
            required=True)

    email = schema.ASCIILine(
            title = _("label_email", default="Email address"),
            required=True)

    password = schema.Password(
            title = _("label_password", default=u"Password"),
            required = True)


class UserPropertyDataManager(grok.MultiAdapter):
    grok.adapts(IPropertiedUser, IField)
    grok.implements(IDataManager)

    def __init__(self, user, field):
        self.user=user
        self.field=field
        self.propname=field.__name__
        for sheet_id in user.listPropertysheets():
            sheet=user.getPropertysheet(sheet_id)
            if sheet.hasProperty(self.propname):
                self.propertysheet=sheet
                break
        else:
            self.propname=None


    def get(self):
        return self.propertysheet.getProperty(self.propname)

    def query(self, default=NO_VALUE):
        if self.propname is None:
            return default
        return self.propertysheet.getProperty(self.propname, NO_VALUE)

    def set(self, value):
        self.propertysheet.setProperty(self.user, self.propname, value)

    def canAccess(self):
        return self.propname is not None

    def canWrite(self):
        return self.propname is not None



class UserPasswordDataManager(grok.MultiAdapter):
    grok.adapts(IPropertiedUser, IPassword)
    grok.implements(IDataManager)

    def __init__(self, user, field):
        self.user=user
        self.field=field

    def get(self):
        raise AttributeError(self.field.__name__)

    def query(self, default=NO_VALUE):
        return default

    def set(self, value):
        if value is None:
            return IStatusMessage(getRequest()).add(
                _('Password not updated, none was specified.'),
                type='error')

        try:
            mt = getToolByName(self.user, "portal_membership")
        except AttributeError:
            return IStatusMessage(getRequest()).add(
                _('Cannot change password for Zope users, only Plone'),
                type='error')
        else:
            mt.setPassword(value)

    def canAccess(self):
        return False

    def canWrite(self):
        return True


class Settings(form.SchemaEditForm):
    grok.context(ISiteRoot)
    grok.name("settings")

    schema = ISettings

    def getContent(self):
        return getSecurityManager().getUser()


