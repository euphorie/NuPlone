from five import grok
from zope.interface import Interface
from z3c.form.interfaces import IGroup
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.utils import mergedTaggedValueList
import plone.z3cform.fieldsets.interfaces


class FormLayoutExtender(grok.MultiAdapter):
    grok.adapts(Interface, Interface, AutoExtensibleForm)
    grok.implements(plone.z3cform.fieldsets.interfaces.IFormExtender)
    grok.name="plonetheme.nuplone.layout"

    order = 10

    def __init__(self, context, request, form):
        self.context=context
        self.request=request
        self.form=form

    def update(self):
        fieldsets=mergedTaggedValueList(self.form.schema, FIELDSETS_KEY)
        if not isinstance(self.form.groups, list):
            self.form.groups=list(self.form.groups)
        groups=dict([(group.__name__, (index, group)) for (index,group) in enumerate(self.form.groups)])
        for fieldset in fieldsets:
            layout=getattr(fieldset, "layout", None)
            if layout is None:
                continue
            if fieldset.__name__ not in groups:
                continue
            (index, group)=groups[fieldset.__name__]

            if not IGroup.providedBy(group):
                group=self.form.groups[index]=group(self.context, self.request, self.form)
            group.layout=layout

