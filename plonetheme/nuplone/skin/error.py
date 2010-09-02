import logging
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_chain
from Acquisition import aq_parent
from five import grok
from zope.browser.interfaces import IBrowserView
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
import zExceptions


log=logging.getLogger(__name__)

grok.templatedir("templates")


class Error(grok.View):
    grok.context(Exception)
    grok.layer(NuPloneSkin)
    grok.name("index.html")
    grok.template("error_generic")

    def update(self):
        self.exception=aq_inner(self.context)
        self.context=context=aq_parent(self)
        if IBrowserView.providedBy(context):
            # NotFound errors can have extra aq wrapping
            self.context=context=aq_parent(context)
        try:
            log.exception("Error at %s", repr(context))
        except zExceptions.Unauthorized:
            pass



class NotFound(Error):
    grok.context(zExceptions.NotFound)
    grok.template("error_notfound")



class Unauthorized(Error):
    grok.context(zExceptions.Unauthorized)
    grok.template("error_unauthorized")

    def authenticate(self):
        """Try to authenticate the user manually, since ZPublisher dropped the
        user whenn it failed to validate access."""
        for parent in aq_chain(aq_inner(self.context)):
            if hasattr(aq_base(parent), "acl_users"):
                uf=parent.acl_users
                try:
                    return uf.validate(self.request, None, roles=["Anonymous"])
                except zExceptions.Unauthorized:
                    pass


    def update(self):
        super(Unauthorized, self).update()
        self.authenticate()

