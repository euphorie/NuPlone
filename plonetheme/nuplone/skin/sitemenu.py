# coding=utf-8
from Acquisition import aq_inner
from OFS.interfaces import ICopyContainer
from plone import api
from plone.memoize.view import memoize_contextless
from plone.protect.utils import addTokenToUrl
from plonetheme.nuplone import MessageFactory as _
from plonetheme.nuplone.utils import getFactoriesInContext
from Products.CMFCore.ActionInformation import ActionInfo
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView


class Sitemenu(BrowserView):
    @property
    @memoize_contextless
    def tools_view(self):
        return api.content.get_view(
            "tools",
            self.context,
            self.request,
        )

    @property
    def settings_url(self):
        return "%s/@@settings" % self.tools_view.navroot_url

    @property
    def view_type(self):
        return self.request.get("view_type", "view")

    def add_submenu(self, menu, submenu):
        """Add a submenu to the menu by extending or adding a category."""
        for item in menu:
            if item["title"] == submenu["title"]:
                item["children"].extend(submenu["children"])
                return
        menu.append(submenu)

    @property
    def actions(self):
        """Helper method to generate the contents for the actions menu."""
        menu = {"title": _("menu_actions", default="Actions")}
        children = menu["children"] = []
        submenu = self.factories()
        if submenu:
            self.add_submenu(children, submenu)
        submenu = self.organise()
        if submenu:
            self.add_submenu(children, submenu)

        if children:
            return menu
        else:
            return None

    def factories(self):
        """Helper method to generate the menu items for creating new content.
        If no content can be created None is returned.
        """
        menu = {"title": _("menu_add_new", default="Add new")}
        children = menu["children"] = []
        actions = getFactoriesInContext(self.context)
        actions.sort(key=lambda x: x.title)
        for action in actions:
            children.append(
                {
                    "title": action.title,
                    "description": action.description,
                    "url": action.url,
                }
            )
        if children:
            return menu
        else:
            return None

    def organise(self):
        """Helper method to generate the menu items for organising content
        (copy/paste/etc.).

        If no organising actions are available None is returned.
        """
        context = aq_inner(self.context)
        context_url = context.absolute_url()
        is_root = ISiteRoot.providedBy(context)
        pa = getToolByName(context, "portal_actions")
        actions = pa.listActions(
            object=context, categories=("object_buttons",), ignore_categories=None
        )
        ec = pa._getExprContext(context)
        actions = [ActionInfo(action, ec) for action in actions]

        menu = {"title": _("menu_organise", default="Organise")}
        children = menu["children"] = []
        for a in actions:
            if a["visible"] and a["allowed"] and a["available"] and not is_root:

                if a["id"] == "copy" and context.cb_isCopyable():
                    children.append(
                        {
                            "title": _("menu_copy", default="Copy"),
                            "url": "%s/@@copy" % context_url,
                        }
                    )

                elif a["id"] == "cut" and context.cb_isMoveable():
                    children.append(
                        {
                            "title": _("menu_cut", default="Cut"),
                            "url": "%s/@@cut" % context_url,
                        }
                    )

                elif a["id"] == "paste" and ICopyContainer.providedBy(context):
                    url = addTokenToUrl("%s/@@paste" % context_url)
                    children.append(
                        {
                            "title": _("menu_paste", default="Paste"),
                            "url": url,
                        }
                    )
                elif a["id"] == "delete":
                    children.append(
                        {
                            "title": _("menu_delete", default="Delete"),
                            "url": "%s/@@delete" % context_url,
                        }
                    )
        if children:
            return menu
