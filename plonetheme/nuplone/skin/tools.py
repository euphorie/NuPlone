from zope.interface import Interface
from five import grok
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone import utils

class Tools(grok.View):
    """Basic view to expose utilties to templates."""

    grok.context(Interface)
    grok.name("tools")
    grok.layer(NuPloneSkin)

    def update(self):
        self.portal=utils.getPortal(self.context)

    def render(self):
        return self

