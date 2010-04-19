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

