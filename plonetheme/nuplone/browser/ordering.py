# coding=utf-8
from Acquisition import aq_inner
from plone.folder.interfaces import IExplicitOrdering
from Products.Five.browser import BrowserView


class UpdateOrder(BrowserView):
    def __call__(self):
        order = self.request.form.get("order[]")
        if not order or not isinstance(order, list):
            return

        orderer = IExplicitOrdering(aq_inner(self.context))
        for (pos, id) in enumerate(order):
            if id == "" or "-" not in id:
                continue
            id = id.split("-", 1)[1]
            orderer.moveObjectToPosition(id, pos)

        return
