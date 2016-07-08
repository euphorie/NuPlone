from zope.component import getMultiAdapter
from zope.component import adapter
from zope.interface import implementer
from five import grok
from ZPublisher.HTTPRequest import FileUpload
from zope.schema.interfaces import IChoice
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from plonetheme.nuplone.z3cform.utils import getVocabulary
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IMultiWidget
from z3c.form.interfaces import IDataManager
from z3c.form.interfaces import NOVALUE
from z3c.form.widget import FieldWidget
from z3c.form.browser.file import FileWidget
from z3c.form.browser.radio import RadioWidget
from z3c.form.browser.select import SelectWidget
from plone.namedfile.interfaces import INamedImageField
from plone.namedfile.interfaces import INamedFileField
from plone.formwidget.namedfile.widget import NamedImageWidget
from plone.formwidget.namedfile.widget import NamedFileWidget

class SingleRadioWidget(RadioWidget):
    """Variant of the z3c.form radio widget which does not pretend a radio
    field can ever return more than one value.

    self.value is still a list since this widget uses the
    SequenceDataConverter. Apparently z3c.form does this since it has no
    concept of a single-valued field which takes its value from a
    vocabulary.
    """

    def update(self):
        super(SingleRadioWidget, self).update()
        for item in self.items:
            item["name"]=item["name"].split(":list", 1)[0]



@adapter(IChoice, INuPloneFormLayer)
@implementer(IFieldWidget)
def ChoiceWidgetFactory(field, request):
    vocabulary=getVocabulary(field)
    if vocabulary is None or len(vocabulary)>4:
        widget=SelectWidget
    else:
        widget=SingleRadioWidget
    return FieldWidget(field, widget(request))



class NewMultiWidgetEntry(grok.View):
    grok.context(IMultiWidget)
    grok.name("new-entry")

    def render(self):
        widget = self.context.getWidget(0)
        return widget.render()



class NicerNamedImageWidget(NamedImageWidget):
    def extract(self, default=NOVALUE):
        action = self.request.get("%s.action" % self.name, None)
        if action == 'remove':
            return None

        value = FileWidget.extract(self, default)

        if value is NOVALUE or \
                (isinstance(value, FileUpload) and not value.filename):
            if self.ignoreContext:
                return default

            dm=getMultiAdapter((self.context, self.field,), IDataManager)
            return dm.get()

        # Note that we allow the user to upload an empty file.
        return value


@adapter(INamedImageField, INuPloneFormLayer)
@implementer(IFieldWidget)
def NamedImageWidgetFactory(field, request):
    return FieldWidget(field, NicerNamedImageWidget(request))


class NicerNamedFileWidget(NamedFileWidget):
    def extract(self, default=NOVALUE):
        action = self.request.get("%s.action" % self.name, None)
        if action == 'remove':
            return None

        value = FileWidget.extract(self, default)

        if value is NOVALUE or \
                (isinstance(value, FileUpload) and not value.filename):
            if self.ignoreContext:
                return default

            dm = getMultiAdapter((self.context, self.field,), IDataManager)
            return dm.get()

        # Note that we allow the user to upload an empty file.
        return value


@adapter(INamedFileField, INuPloneFormLayer)
@implementer(IFieldWidget)
def NamedFileWidgetFactory(field, request):
    return FieldWidget(field, NicerNamedFileWidget(request))
