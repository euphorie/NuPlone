from plone.app.layout.navigation.interfaces import INavigationRoot
from Acquisition import aq_inner
from Acquisition import aq_chain

def getNavigationRoot(context):
    for obj in aq_chain(aq_inner(context)):
        if INavigationRoot.providedBy(obj):
            break
    return obj

