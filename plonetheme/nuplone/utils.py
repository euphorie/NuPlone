from Acquisition import aq_inner
from Acquisition import aq_chain
from AccessControl import getSecurityManager
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.interfaces import IPloneSiteRoot

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



