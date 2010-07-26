from Acquisition import aq_inner
from plone.tiles import Tile
from plonetheme.nuplone.utils import getNavigationRoot
from Products.CMFPlone.utils import typesToList
from Products.CMFCore.utils import getToolByName

class TabsTile(Tile):
    def getRoot(self):
        return getNavigationRoot(self.context)


    def update(self):
        context=aq_inner(self.context)
        contextUrl=context.absolute_url()
        navroot=self.getRoot()
        navrootPath="/".join(navroot.getPhysicalPath())
        portal_properties=getToolByName(self.context, "portal_properties")
        use_view_types=portal_properties.site_properties.typesUseViewActionInListings

        query={}
        query["path"]=dict(query=navrootPath, depth=1)
        query["portal_type"]=typesToList(context)
        query["sort_on"]="getObjPositionInParent"
        query["sort_order"]="asc"
        query["is_default_page"]=False

        catalog=getToolByName(context, "portal_catalog")
        results=[{"id" : brain.id,
                  "title" : brain.Title,
                  "url" : "%s/view" % brain.getURL() if brain.portal_type in use_view_types else brain.getURL(),
                  "class" : None}
                 for brain in catalog.searchResults(query)
                 if not brain.exclude_from_nav]
        current=[(len(result["url"]), result["id"]) for result in results
                 if contextUrl.startswith(result["url"])]
        current.sort()
        if current:
            current=current[0][1]
            for result in results:
                if result["id"]==current:
                    result["class"]="current"
                    break

        self.tabs=results
        self.home_url=navroot.absolute_url()


    def __call__(self):
        self.update()
        return self.index()
