import logging
from Acquisition import aq_inner
from Acquisition import aq_chain
from AccessControl import getSecurityManager
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName

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
    one of three options: ``view`` for normal object views, ``edit``
    for edit forms, and ``other`` for all other types."""
# XXX How to check for add views?

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


