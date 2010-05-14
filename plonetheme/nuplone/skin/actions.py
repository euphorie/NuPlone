from Acquisition import aq_inner
from Acquisition import aq_parent
import zExceptions
from ZODB.POSException import ConflictError
from OFS.interfaces import ICopySource
from OFS.interfaces import ICopyContainer
from OFS.CopySupport import CopyError
from five import grok
from Products.statusmessages.interfaces import IStatusMessage
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone import MessageFactory as _


class Copy(grok.View):
    grok.context(ICopySource)
    grok.layer(NuPloneSkin)
    grok.require("zope2.CopyOrMove")
    grok.name("copy")

    def render(self):
        context=aq_inner(self.context)
        container=aq_parent(context)
        if not context.cb_isCopyable():
            raise zExceptions.Unauthorized

        container.manage_copyObjects(context.getId(), self.request)
        flash=IStatusMessage(self.request).addStatusMessage
        flash(_(u"message_copy_sucess", default=u"Copied"), "notice")
        self.request.response.redirect(context.absolute_url())



class Cut(grok.View):
    grok.context(ICopySource)
    grok.layer(NuPloneSkin)
    grok.require("zope2.CopyOrMove")
    grok.name("cut")

    def render(self):
        context=aq_inner(self.context)
        container=aq_parent(context)
        flash=IStatusMessage(self.request).addStatusMessage

        try:
            container.manage_cutObjects(context.getId(), self.request)
            flash(_("message_cut_success", default=u"Cut."), "notice")
        except CopyError:
            flash(_("message_cut_invalid", default=u"It is not possible to move this object."), "error")



class Paste(grok.View):
    grok.context(ICopyContainer)
    grok.layer(NuPloneSkin)
    grok.require("zope2.CopyOrMove")
    grok.name("paste")

    def render(self):
        context=aq_inner(self.context)
        flash=IStatusMessage(self.request).addStatusMessage
        if not context.cb_dataValid():
            raise zExceptions.Unauthorized

        try:
            context.manage_pasteObjects(REQUEST=self.request)
            flash(_("message_paste_succes", default=u"Pasted"), "success")
        except ConflictError:
            raise
        except ValueError:
            flash(_("message_paste_valueerror", default=u"You can not paste the copied data here."), "error")
        except zExceptions.Unauthorized:
            flash(_("message_paste_unauthorized", default=u"You can not allowed to paste here."), "error")
        except CopyError:
            flash(_("message_paste_generic", default=u"No valid date found in the clipboard."), "error")

        self.request.response.redirect(context.absolute_url())

