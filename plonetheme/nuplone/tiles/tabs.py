from plone.tiles import Tile
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.navigation.root import getNavigationRootObject
from Products.CMFPlone.utils import typesToList
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

class TabsTile(Tile):
    def update(self):
        context=aq_inner(self.context)
        navrootPath=getNavigationRoot(context)
        navrootUrl=navrootPath

        query={}
        query["path"]=dict(query=navrootPath, depth=1)
        query["portal_type"]=typesToList(context)
        query["sort_on"]="getObjPositionInParent"
        query["sort_order"]="asc"
        query["is_default_page"]=False

        catalog=getToolByName(context, "portal_catalog")
        results=[brain for brain in catalog.searchResults(query)
                 if not brain.exclude_from_nav]

        self.tabs=[]


    def __call__(self):
        self.update()
        return self.index()
