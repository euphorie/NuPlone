from Acquisition import aq_inner
from zope.interface import Interface
from five import grok
from plonetheme.nuplone import MessageFactory as _
from plonetheme.nuplone.utils import getPortal
from plonetheme.nuplone.utils import setLanguage
from Products.statusmessages.interfaces import IStatusMessage


class SwitchLanguage(grok.View):
    grok.context(Interface)
    grok.require('zope2.Public')
    grok.name('switch-language')

    def render(self):
        flash = IStatusMessage(self.request).addStatusMessage
        if setLanguage(self.request, self.context):
            flash(_('message_switch_language',
                default=u'Language updated'), 'success')
        else:
            flash(_('message_switch_language_error',
                default=u'Failed to switch language'), 'error')

        next_url = self.request.get('came_from')
        if not next_url:
            next_url = self.request.environ.get('HTTP_REFERER')
        if not next_url or not \
                next_url.startswith(getPortal(self.context).absolute_url()):
            next_url = aq_inner(self.context).absolute_url()

        self.request.response.redirect(next_url)
