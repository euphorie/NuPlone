import collections
import martian
from five import grok
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope import component
from z3c.form.interfaces import IGroup
from z3c.form.interfaces import IWidget
from z3c.form.browser.checkbox import CheckBoxWidget
from plone.autoform.form import AutoExtensibleForm
from plone.directives.form.schema import FormMetadataListStorage
from plone.directives.form import Schema
from plone.directives.form.schema import TEMP_KEY
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.utils import mergedTaggedValueList
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.interfaces import IDexterityContent
from plone.behavior.interfaces import IBehavior
import plone.z3cform.fieldsets.interfaces

Dependency = collections.namedtuple("Dependency", "name field op value action")
DEPENDENCY_KEY = "plonetheme.nuplone.z3cform.dependency"
LAYOUT_KEY = "plonetheme.nuplone.z3cform.layout"


class depends(martian.Directive):
    """Directive used to declare a dependency on other field values."""
    scope = martian.CLASS
    store = FormMetadataListStorage()
    key = DEPENDENCY_KEY

    def factory(self, field, name, op="on", value=None, action="show"):
        if op not in [ "on", "off", "==", "!=" ]:
            raise ValueError("Invalid operand given")
        if action not in [ "show", "enable" ]:
            raise ValueError("Invalid action given")
        return [Dependency(field, name, op, value, action)]


class FormSchemaGrokker(martian.InstanceGrokker):
    """Grok form schema hints."""
    martian.component(Schema.__class__)
    martian.directive(depends)

    def execute(self, interface, config, **kw):
        if not interface.extends(Schema):
            return False

        # Copy from temporary to real value
        directiveSupplied = interface.queryTaggedValue(TEMP_KEY, None)
        if directiveSupplied is not None:
            for key, tgv in directiveSupplied.items():
                existingValue = interface.queryTaggedValue(key, None)

                if existingValue is not None:
                    if type(existingValue) != type(tgv):
                        # Don't overwrite if we have a different type
                        continue
                    elif isinstance(existingValue, list):
                        existingValue.extend(tgv)
                        tgv = existingValue
                    elif isinstance(existingValue, dict):
                        existingValue.update(tgv)
                        tgv = existingValue

                interface.setTaggedValue(key, tgv)

            interface.setTaggedValue(TEMP_KEY, None)
        return True


class FormDependencyExtender(grok.MultiAdapter):
    grok.adapts(Interface, Interface, AutoExtensibleForm)
    grok.implements(plone.z3cform.fieldsets.interfaces.IFormExtender)
    grok.name("plonetheme.nuplone.dependency")
    order = 0

    def __init__(self, context, request, form):
        self.context=context
        self.request=request
        self.form=form

    def update(self):
        schemas = [self.form.schema]

        if IDexterityContent.providedBy(self.context):
            fti = component.getUtility(
                IDexterityFTI,
                name=self.context.portal_type)
            for name in fti.behaviors:
                behavior = component.queryUtility(IBehavior, name=name)
                if behavior and behavior.interface.extends(Schema):
                    schemas.append(behavior.interface)

        directives = []
        for schema in schemas:
            directives += mergedTaggedValueList(schema, DEPENDENCY_KEY)

        dependencies = {}
        for directive in directives:
            dependencies.setdefault(directive.name, []).append(directive)

        todo=collections.deque([self.form])
        while todo:
            group=todo.pop()
            if hasattr(group, "groups"):
                todo.extendleft(group.groups)
            for (name, field) in group.fields.items():
                depends=dependencies.get(name, None)
                if depends is None:
                    continue
                field.field._dependencies=depends


class WidgetDependencyView(grok.MultiAdapter):
    grok.adapts(IWidget, Interface)
    grok.implements(IBrowserView)
    grok.name("dependencies")

    def __init__(self, widget, request):
        self.widget=widget
        self.request=request

    def __call__(self):
        dependencies=getattr(self.widget.field, "_dependencies", None)
        if not dependencies:
            return None

        classes=[]
        widgets=self.widget.__parent__
        for dependency in dependencies:
            widget=widgets[dependency.field]
            name=widget.name
            if isinstance(widget, CheckBoxWidget):
                name="%s:list" % name
            if dependency.op in [ "on", "off"]:
                classes.append("dependsOn-%s-%s" % (name, dependency.op))
            elif dependency.op=="==":
                classes.append("dependsOn-%s-equals-%s" % (name, dependency.value))
            elif dependency.op=="!=":
                classes.append("dependsOn-%s-notEquals-%s" % (name, dependency.value))

            classes.append("dependsAction-%s" % dependency.action)

        return " ".join(classes) if classes else None


class FormLayoutExtender(grok.MultiAdapter):
    grok.adapts(Interface, Interface, AutoExtensibleForm)
    grok.implements(plone.z3cform.fieldsets.interfaces.IFormExtender)
    grok.name("plonetheme.nuplone.layout")

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


