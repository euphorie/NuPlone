# coding=utf-8
from Acquisition import aq_inner
from plone import api
from plone.tiles import Tile
from plonetheme.nuplone.utils import getNavigationRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import typesToList
from zExceptions import NotFound


class TabsTile(Tile):
    def getRoot(self):
        return getNavigationRoot(self.context)

    def update(self):
        context = aq_inner(self.context)
        contextUrl = context.absolute_url()
        navroot = self.getRoot()
        navrootPath = "/".join(navroot.getPhysicalPath())
        use_view_types = api.portal.get_registry_record(
            "plone.types_use_view_action_in_listings", default=[]
        )
        query = {}
        query["path"] = dict(query=navrootPath, depth=1)
        query["portal_type"] = typesToList(context)
        query["sort_on"] = "getObjPositionInParent"
        query["sort_order"] = "asc"
        query["is_default_page"] = False

        catalog = getToolByName(context, "portal_catalog")
        results = [
            {
                "id": brain.id,
                "title": brain.Title,
                "url": "%s/view" % brain.getURL()
                if brain.portal_type in use_view_types
                else brain.getURL(),
                "class": None,
            }
            for brain in catalog.searchResults(query)
            if not brain.exclude_from_nav
        ]
        current = sorted(
            [
                (len(result["url"]), result["id"])
                for result in results
                if contextUrl.startswith(result["url"])
            ]
        )
        if current:
            current = current[0][1]
            for result in results:
                if result["id"] == current:
                    result["class"] = "current"
                    break

        self.tabs = results
        self.home_url = navroot.absolute_url()

    def __call__(self):
        if isinstance(self.context, NotFound):
            return ""
        self.update()
        return self.index()
