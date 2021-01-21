# coding=utf-8
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.tiles import Tile
from plonetheme.nuplone.utils import getNavigationRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import typesToList
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface

import collections


class INavtreeFactory(Interface):
    """Marker interface for catalog builder functions."""

    def __call__(context, request):
        """Return a CatalogNavTree instance."""


class CatalogNavTree(object):
    def __init__(self, context, request):
        self.build(context, request)

    def build(self, context, request):
        context = aq_inner(context)

        # If we are at a default page use the folder as context for the navtree
        container = aq_parent(context)
        isp = queryMultiAdapter((container, request), name="default_page", default=None)
        if isp is not None and isp.isDefaultPage(context):
            context = container

        contextPath = "/".join(context.getPhysicalPath())
        contextPathLen = len(contextPath)
        parentDepth = contextPath.count("/") - 1
        navrootPath = "/".join(getNavigationRoot(context).getPhysicalPath())

        query = {}
        query["path"] = dict(
            query=contextPath, navtree=True, navtree_start=navrootPath.count("/")
        )
        query["portal_type"] = typesToList(context)
        query["sort_on"] = "getObjPositionInParent"
        query["sort_order"] = "asc"

        catalog = getToolByName(context, "portal_catalog")
        results = catalog.searchResults(query)
        cache = {}
        cache[navrootPath] = {"current": False, "currentParent": True, "children": []}
        for brain in results:
            path = brain.getPath()
            pathLen = len(path)
            parentPath = path.rsplit("/", 1)[0]
            ancestor = current = currentParent = False
            if path == contextPath:
                current = True
            elif contextPathLen > pathLen:
                ancestor = contextPath.startswith(path + "/")
                currentParent = ancestor and path.count("/") == parentDepth

            if brain.exclude_from_nav and not currentParent:
                continue

            oldNode = cache.get(path, None)
            node = {
                "brain": brain,
                "path": path,
                "current": current,
                "currentParent": currentParent,
                "ancestor": ancestor,
            }

            oldNode = cache.get(path, None)
            if oldNode is not None:
                oldNode.update(node)
                node = oldNode
            else:
                node["children"] = []
                cache[path] = node

            parentNode = cache.get(parentPath, None)
            if parentNode is None:
                parentNode = cache[parentPath] = dict(children=[node])
            else:
                parentNode["children"].append(node)
            node["parent"] = parentNode

        self.tree = cache
        self.root = cache[navrootPath]

    def __iter__(self):
        """Breadth-first iterator for navtree nodes which allows
        modifications of the tree during iteration. Modifications
        are given by passing a command to the next() method of the
        generator. For example:

        >>> tree=CatalogNavTree(context, request)
        >>> g=tree.iter()
        >>> value=next(g)
        >>> try:
        ...     while True:
        ...        if value.portal_type=="Collection":
        ...            value=g.send("prune")
        ...        else:
        ...            value=next(g)
        ... except StopIteration:
        ...     pass

        The supported commands are:

        * purge: remove the node and all its children from the tree
        * prune: remove all children of this node from the tree

        In addition you may also modify the datastructures directly
        during iteration.
        """
        queue = collections.deque([self.root])
        while queue:
            node = queue.popleft()
            action = yield node
            if action == "purge":
                node["parent"]["children"].remove(node)
                continue
            elif action == "prune":
                node["children"] = []
                continue

            for child in node.get("children", []):
                queue.append(child)

    iter = __iter__


@implementer(INavtreeFactory)
@adapter(Interface, Interface)
class TreeFactory(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return CatalogNavTree(self.context, self.request)


class NavigationTile(Tile):
    def update(self):
        portal_types = getToolByName(self.context, "portal_types")
        type_titles = dict(
            [(fti.getId(), fti.Title()) for fti in portal_types.listTypeInfo()]
        )

        use_view_types = api.portal.get_registry_record(
            "plone.types_use_view_action_in_listings", default=[]
        )
        normalize = getUtility(IIDNormalizer).normalize
        treefactory = getMultiAdapter((self.context, self.request), INavtreeFactory)
        tree = treefactory()

        for node in tree.iter():
            brain = node.get("brain", None)
            if brain is None:
                continue
            node["title"] = brain.Title
            node["description"] = brain.Description or None
            node["portal_type"] = normalize(brain.portal_type)
            node["portal_type_title"] = type_titles.get(
                brain.portal_type, brain.portal_type
            )
            node["url"] = (
                "%s/view" % brain.getURL()
                if brain.portal_type in use_view_types
                else brain.getURL()
            )
            node["review_state"] = normalize(brain.review_state)
            node["folderish"] = brain.is_folderish
            node["class"] = (
                " ".join(
                    filter(
                        None,
                        [
                            "active"
                            if node["current"] or node["currentParent"]
                            else None,
                            "current" if node["current"] else None,
                        ],
                    )
                )
                or None
            )

        if "brain" in tree.root:
            self.tree = [tree.root]
        else:
            self.tree = tree.root["children"]

    def __call__(self):
        self.update()
        return self.index()
