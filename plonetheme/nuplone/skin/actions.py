from Acquisition import aq_inner
from Acquisition import aq_parent
from OFS.CopySupport import CopyError
from plonetheme.nuplone import MessageFactory as _
from plonetheme.nuplone.utils import checkPermission
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from ZODB.POSException import ConflictError
from zope.component import getMultiAdapter

import zExceptions


class Copy(BrowserView):
    def __call__(self):
        context = aq_inner(self.context)
        container = aq_parent(context)
        if not context.cb_isCopyable():
            raise zExceptions.Unauthorized

        container.manage_copyObjects(context.getId(), self.request)
        flash = IStatusMessage(self.request).addStatusMessage
        flash(_(u"message_copy_sucess", default=u"Copied"), "notice")
        self.request.response.redirect(context.absolute_url())


class Cut(BrowserView):
    def __call__(self):
        context = aq_inner(self.context)
        container = aq_parent(context)
        flash = IStatusMessage(self.request).addStatusMessage

        try:
            container.manage_cutObjects(context.getId(), self.request)
            flash(_("message_cut_success", default=u"Cut."), "notice")
        except CopyError:
            flash(
                _(
                    "message_cut_invalid",
                    default=u"It is not possible to move this object.",
                ),
                "error",
            )

        self.request.response.redirect(context.absolute_url())


class Paste(BrowserView):
    def __call__(self):
        context = aq_inner(self.context)
        flash = IStatusMessage(self.request).addStatusMessage
        if not context.cb_dataValid():
            raise zExceptions.Unauthorized

        try:
            context.manage_pasteObjects(REQUEST=self.request)
            flash(_("message_paste_succes", default=u"Pasted"), "success")
        except ConflictError:
            raise
        except ValueError:
            flash(
                _(
                    "message_paste_valueerror",
                    default=u"You can not paste the copied data here.",
                ),
                "error",
            )
        except zExceptions.Unauthorized:
            flash(
                _(
                    "message_paste_unauthorized",
                    default=u"You are not allowed to paste here.",
                ),
                "error",
            )
        except CopyError as e:
            if "Insufficient Privileges" in e.message:
                raise zExceptions.Unauthorized
            flash(
                _(
                    "message_paste_generic",
                    default=u"No valid data found in the clipboard.",
                ),
                "error",
            )

        self.request.response.redirect(context.absolute_url())


class Delete(BrowserView):
    def verify(self, container, context):
        if not checkPermission(container, "Delete objects"):
            raise zExceptions.Unauthorized

        return True

    def post(self):
        action = self.request.form.get("action", "cancel")
        context = aq_inner(self.context)
        flash = IStatusMessage(self.request).addStatusMessage

        if action == "cancel":
            flash(_("message_delete_cancel", default=u"Deletion cancelled"), "notice")
            self.request.response.redirect(context.absolute_url())
        elif action == "delete":
            authenticator = getMultiAdapter(
                (self.context, self.request), name=u"authenticator"
            )
            if not authenticator.verify():
                raise zExceptions.Unauthorized

            container = aq_parent(context)
            container.manage_delObjects([context.getId()])
            flash(_("message_delete_success", default=u"Object removed"), "success")
            self.request.response.redirect(container.absolute_url())

    def __call__(self):
        context = aq_inner(self.context)
        container = aq_parent(context)

        if not self.verify(container, context):
            return

        if self.request.method == "POST":
            return self.post()
        return super(Delete, self).__call__()
