from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Five import BrowserView
from zope.browser.interfaces import IBrowserView

import logging
import zExceptions


log = logging.getLogger(__name__)


class Error(BrowserView):
    def update(self):
        self.exception = aq_inner(self.context)
        self.context = context = aq_parent(self)
        if IBrowserView.providedBy(context):
            # NotFound errors can have extra aq wrapping
            self.context = context = aq_parent(context)
        log.debug("%r -> %r", self.exception, context)

    def __call__(self):
        self.update()
        return super(Error, self).__call__()


class Unauthorized(Error):
    def authenticate(self):
        """Try to authenticate the user manually, since ZPublisher dropped the
        user when it failed to validate access."""
        for parent in aq_chain(aq_inner(self.context)):
            if hasattr(aq_base(parent), "acl_users"):
                uf = parent.acl_users
                try:
                    return uf.validate(self.request, None, roles=["Anonymous"])
                except zExceptions.Unauthorized:
                    pass

    def update(self):
        super(Unauthorized, self).update()
        self.authenticate()
