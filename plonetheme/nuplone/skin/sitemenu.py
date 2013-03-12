from five import grok
from zope.interface import Interface

from Acquisition import aq_inner
from OFS.interfaces import ICopyContainer

from Products.CMFCore.ActionInformation import ActionInfo
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

from plonetheme.nuplone import MessageFactory as _
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.utils import getFactoriesInContext

grok.templatedir("templates")


class Sitemenu(grok.View):
    grok.context(Interface)
    grok.name("sitemenu")
    grok.layer(NuPloneSkin)
    grok.template("sitemenu")

    @property
    def settings_url(self):
        return "%s/@@settings" % self.navroot_url

    def update(self):
        self.view_type = self.request.get("view_type", "view")
        self.actions = self.actions()

    def actions(self):
        """Helper method to generate the contents for the actions menu.
        """
        menu = {"title": _("menu_actions", default=u"Actions")}
        children = menu["children"] = []
        submenu = self.factories()
        if submenu:
            children.append(submenu)
        submenu = self.organise()
        if submenu:
            children.append(submenu)

        if children:
            return menu
        else:
            return None

    def factories(self):
        """Helper method to generate the menu items for creating new content.
        If no content can be created None is returned.
        """
        menu = {"title": _("menu_add_new", default=u"Add new")}
        children = menu["children"] = []
        actions = getFactoriesInContext(self.context)
        actions.sort(key=lambda x: x.title)
        for action in actions:
            children.append({"title": action.title,
                             "description": action.description,
                             "url": action.url,
                            })
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
        pa = getToolByName(context, 'portal_actions')
        actions = pa.listActions(object=context,
                                 categories=('folder_buttons',),
                                 ignore_categories=None)
        ec = pa._getExprContext(context)
        actions = [ActionInfo(action, ec) for action in actions]

        menu = {"title": _("menu_organise", default=u"Organise")}
        children = menu["children"] = []
        for a in actions:
            if a['visible'] and a['allowed'] \
                    and a['available'] and not is_root:

                if a['id'] == 'copy' and context.cb_isCopyable():
                    children.append({"title": _("menu_copy", default=u"Copy"),
                                    "url": "%s/@@copy" % context_url})

                elif a['id'] == 'cut' and context.cb_isMoveable():
                    children.append({"title": _("menu_cut", default=u"Cut"),
                                    "url": "%s/@@cut" % context_url})

                elif a['id'] == 'paste' and ICopyContainer.providedBy(context):
                    children.append({
                        "title": _("menu_paste", default=u"Paste"),
                        "url": "%s/@@paste" % context_url
                    })
                elif a['id'] == 'delete':
                    children.append({
                        "title": _("menu_delete", default=u"Delete"),
                        "url": "%s/@@delete" % context_url
                    })
        if children:
            return menu
