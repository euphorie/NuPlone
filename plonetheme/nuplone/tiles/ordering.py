from Acquisition import aq_inner
from five import grok
from plone.folder.interfaces import IExplicitOrdering
from plone.folder.interfaces import IOrderableFolder
from plonetheme.nuplone.skin.interfaces import NuPloneSkin


class UpdateOrder(grok.View):
    grok.context(IOrderableFolder)
    grok.name("update-order")
    grok.require("cmf.ModifyPortalContent")
    grok.layer(NuPloneSkin)

    def render(self):
        order=self.request.form.get("order[]")
        if not order or not isinstance(order, list):
            return

        orderer=IExplicitOrdering(aq_inner(self.context))
        for (pos, id) in enumerate(order):
            id=id.split("-", 1)[1]
            orderer.moveObjectToPosition(id, pos)

        return
