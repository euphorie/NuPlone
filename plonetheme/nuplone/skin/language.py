from Acquisition import aq_inner
from plonetheme.nuplone import MessageFactory as _
from plonetheme.nuplone.utils import setLanguage
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage


class SwitchLanguage(BrowserView):
    def __call__(self):
        flash = IStatusMessage(self.request).addStatusMessage
        if setLanguage(self.request, self.context):
            flash(_("message_switch_language", default="Language updated"), "success")
        else:
            flash(
                _(
                    "message_switch_language_error",
                    default="Failed to switch language",
                ),
                "error",
            )

        next_url = self.request.get("came_from")
        if not next_url:
            next_url = self.request.environ.get("HTTP_REFERER")
        put = getToolByName(self.context, "portal_url")
        if not next_url or not put.isURLInPortal(next_url):
            next_url = aq_inner(self.context).absolute_url()

        self.request.response.redirect(next_url)
