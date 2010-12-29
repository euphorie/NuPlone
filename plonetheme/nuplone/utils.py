import collections
import logging
from email.MIMEText import MIMEText
from email.Header import Header
import email.utils as emailutils
from Acquisition import aq_inner
from Acquisition import aq_chain
from AccessControl import getSecurityManager
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.ActionInformation import ActionInfo
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from plonetheme.nuplone import MessageFactory as _

log = logging.getLogger(__name__)


def getPortal(context):
    for obj in aq_chain(aq_inner(context)):
        if IPloneSiteRoot.providedBy(obj):
            return obj


def getNavigationRoot(context):
    for obj in aq_chain(aq_inner(context)):
        if INavigationRoot.providedBy(obj):
            break
    return obj


def checkPermission(context, permission):
    return getSecurityManager().checkPermission(permission, context)


def isAnonymous(user=None):
    if user is None:
        user=getSecurityManager().getUser()
    return user is None or user.getUserName()=="Anonymous User"


def viewType(context, request):
    """Determine what type of view the user is looking at. This returns
    one of three options: ``view`` for normal object views, ``add``
    for add forms, ``edit`` for edit forms, and ``other`` for all other
    types."""

    view=request.other.get("PUBLISHED")
    if view is not None:
        if IAddForm.providedBy(view):
            return "add"
        if IEditForm.providedBy(view):
            return "edit"

    for url in [ "ACTUAL_URL", "VIRTUAL_URL", "URL" ]:
        current_url=request.get(url)
        if current_url is not None:
            break
    else:
        return "view"

    if current_url.endswith("/"):
        current_url=current_url[:-1]

    if current_url.endswith("@@edit"):
        return "edit"
    elif "/++add++" in current_url:
        return "add"

    if current_url==aq_inner(context).absolute_url():
        return "view"

    return "other"



class SimpleLiteral(unicode):
    def __html__(self):
        return unicode(self)



def setLanguage(request, context, lang=None):
    """Switch Plone to another language. If no language is given via the
    `lang` parameter the language is taken from a `language`
    request parameter. If a dialect was chosen but is not available the main
    language is used instead. If the main language is also not available
    nothing is done and ``False`` is returned.

    It is safe to call this method before rendering a template: it will
    immediately switch the current language. That means there is no need
    to trigger a redirect to force a new HTTP request. 
    """
    if lang is None:
        lang=request.form.get("language")
    if not lang:
        return

    lang=lang.lower()
    lt=getToolByName(context, "portal_languages")
    res=lt.setLanguageCookie(lang=lang)
    if res is None and "-" in lang:
        lang=lang.split("-")[0]
        res=lt.setLanguageCookie(lang=lang)
        if res is None:
            log.warn("Failed to switch language to %s", lang)
            return False

    # In addition to setting the cookie also update the PTS language.
    # This effectively switches Plone over to the new language without
    # requiring a new HTTP request.
    request["LANGUAGE"]=lang
    binding=request.get("LANGUAGE_TOOL", None)
    if binding is not None:
        binding.LANGUAGE=lang

    return True


FactoryInfo = collections.namedtuple("FactoryInfo", "id title description url")

def getFactoriesInContext(context):
    """Return a list of all factories available to the current user at
    the given location."""
    context=aq_inner(context)
    ftis=context.allowedContentTypes()
    if not ftis:
        return []

    tt=getToolByName(context, "portal_types")
    ec=tt._getExprContext(context)
    actions=[ActionInfo(fti, ec) for fti in ftis]
    actions=[FactoryInfo(action.get("id"),
                         action.get("title") or action.get("id"), 
                         action.get("description") or None,
                         action["url"])
             for action in actions]
    return actions


def createEmailTo(sender_name, sender_email, recipient_name, recipient_email,
                  subject, body, format="plain"):
    """Create an :obj:`email.MIMEText.MIMEtext` instance for an email. This
    method will take care of adding addings a date header and message ID
    to the email, as well as quoting of non-ASCII content.
    """
    if isinstance(body, unicode):
        mail=MIMEText(body.encode("utf-8"), format, "utf-8")
    else:
        mail=MIMEText(body, format)

    if sender_name:
        mail["From"]=emailutils.formataddr((sender_name, sender_email))
    else:
        mail["From"]=sender_email
    if recipient_name:
        mail["To"]=emailutils.formataddr((recipient_name, recipient_email))
    else:
        mail["To"]=recipient_email
    mail["Subject"]=Header(subject.encode("utf-8"), "utf-8")
    mail["Message-Id"]=emailutils.make_msgid()
    mail["Date"]=emailutils.formatdate(localtime=True)
    mail.set_param("charset", "utf-8")

    return mail


class reify(object):
    """ Put the result of a method which uses this (non-data)
    descriptor decorator in the instance dict after the first call,
    effectively replacing the decorator with an instance variable."""
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


def formatDate(request, date, length="long"):
    """Wrapper aound the zope.i18n date formatter which does not abort on
    pre-1900 dates.
    """
    if date.year<1900:
        return _("date_to_early", default=u"<pre-1900-date>")
    return request.locale.dates.getFormatter("date", length).format(date)


def formatTime(request, time, length=None):
    return request.locale.dates.getFormatter("time", length).format(time)


def formatDatetime(request, timestamp, length="long"):
    """Wrapper aound the zope.i18n datetime formatter which does not abort on
    pre-1900 dates.
    """
    if timestamp.year<1900:
        return _("date_to_early", default=u"<pre-1900-date>")
    if length=="long":
        return _("format_datetime", default="${date} at ${time}",
                mapping=dict(date=formatDate(request, timestamp, "long"),
                             time=formatTime(request, timestamp, "short")))
    return request.locale.dates.getFormatter("dateTime", length).format(timestamp)

