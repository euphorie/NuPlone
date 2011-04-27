from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.interface import Interface
from five import grok
from AccessControl.Permissions import copy_or_move
from AccessControl.Permissions import delete_objects
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.utils import checkPermission
from plonetheme.nuplone.utils import getFactoriesInContext
from plonetheme.nuplone import MessageFactory as _
from Products.CMFCore.interfaces import ISiteRoot
from OFS.interfaces import ICopyContainer
from OFS.interfaces import ICopySource


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
        self.view_type=self.request.get("view_type", "view")
        self.actions=self.actions()


    def actions(self):
        """Helper method to generate the contents for the actions menu.
        """
        menu={"title": _("menu_actions", default=u"Actions")}
        children=menu["children"]=[]
        submenu=self.factories()
        if submenu:
            children.append(submenu)
        submenu=self.organise()
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
        menu={"title": _("menu_add_new", default=u"Add new")}
        children=menu["children"]=[]
        actions=getFactoriesInContext(self.context)
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
        context=aq_inner(self.context)
        context_url=context.absolute_url()
        parent=aq_parent(context)
        is_root=ISiteRoot.providedBy(context)
        is_copyable=not is_root and ICopySource.providedBy(context) and checkPermission(context, copy_or_move)
        can_delete=not is_root and checkPermission(parent, delete_objects)
        can_copy=is_copyable and context.cb_isCopyable()
        can_cut=is_copyable and can_delete and context.cb_isMoveable()
        can_paste=ICopyContainer.providedBy(context) and context.cb_dataValid()

        menu={"title": _("menu_organise", default=u"Organise")}
        children=menu["children"]=[]
        if can_copy:
            children.append({"title": _("menu_copy", default=u"Copy"),
                             "url": "%s/@@copy" % context_url})
        if can_cut:
            children.append({"title": _("menu_cut", default=u"Cut"),
                             "url": "%s/@@cut" % context_url})
        if can_paste:
            children.append({"title": _("menu_paste", default=u"Paste"),
                             "url": "%s/@@paste" % context_url})
        if can_delete:
            children.append({"title": _("menu_delete", default=u"Delete"),
                             "url": "%s/@@delete" % context_url})
        if children:
            return menu
        else:
            return None

