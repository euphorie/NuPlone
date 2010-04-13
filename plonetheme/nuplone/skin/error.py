import logging
from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
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
        self.context=aq_parent(self)
        log.exception("Error at %r", self.context)


class NotFound(Error):
    grok.context(zExceptions.NotFound)
    grok.template("error_notfound")


class Unauthorized(Error):
    grok.context(zExceptions.Unauthorized)
    grok.template("error_unauthorized")

