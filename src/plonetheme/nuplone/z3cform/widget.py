from plone.formwidget.namedfile.widget import NamedFileWidget
from plone.formwidget.namedfile.widget import NamedImageWidget
from plone.namedfile.interfaces import INamedFileField
from plone.namedfile.interfaces import INamedImageField
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from plonetheme.nuplone.z3cform.utils import getVocabulary
from Products.Five import BrowserView
from z3c.form.browser.file import FileWidget
from z3c.form.browser.radio import RadioWidget
from z3c.form.browser.select import SelectWidget
from z3c.form.interfaces import IDataManager
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import NOVALUE
from z3c.form.widget import FieldWidget
from ZODB.POSException import POSKeyError
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import implementer_only
from zope.schema.interfaces import IChoice
from ZPublisher.HTTPRequest import FileUpload

import Acquisition
import z3c.form.browser.textarea
import z3c.form.interfaces
import z3c.form.widget
import zope.interface
import zope.schema.interfaces


class SingleRadioWidget(RadioWidget):
    """Variant of the z3c.form radio widget which does not pretend a radio
    field can ever return more than one value.

    self.value is still a list since this widget uses the
    SequenceDataConverter. Apparently z3c.form does this since it has no
    concept of a single-valued field which takes its value from a
    vocabulary.
    """

    def update(self):
        super().update()
        for item in self.items:
            item["name"] = item["name"].split(":list", 1)[0]


@adapter(IChoice, INuPloneFormLayer)
@implementer(IFieldWidget)
def ChoiceWidgetFactory(field, request):
    vocabulary = getVocabulary(field)
    if vocabulary is None or len(vocabulary) > 4:
        widget = SelectWidget
    else:
        widget = SingleRadioWidget
    return FieldWidget(field, widget(request))


class NewMultiWidgetEntry(BrowserView):
    def __call__(self):
        widget = self.context.getWidget(0)
        return widget.render()


class NicerNamedImageWidget(NamedImageWidget):
    @property
    def allow_nochange(self):
        # Prevent errors caused by missing blob file
        if self.value != self.field.missing_value:
            try:
                blob = getattr(self.value, "_blob", None)
                if blob:
                    blob.__repr__()
            except POSKeyError:
                return False
        return super().allow_nochange

    def extract(self, default=NOVALUE):
        action = self.request.get("%s.action" % self.name, None)
        if action == "remove":
            return None

        value = FileWidget.extract(self, default)

        if value is NOVALUE or (isinstance(value, FileUpload) and not value.filename):
            if self.ignoreContext:
                return default

            dm = getMultiAdapter(
                (
                    self.context,
                    self.field,
                ),
                IDataManager,
            )
            return dm.get()

        # Note that we allow the user to upload an empty file.
        return value


@adapter(INamedImageField, INuPloneFormLayer)
@implementer(IFieldWidget)
def NamedImageWidgetFactory(field, request):
    return FieldWidget(field, NicerNamedImageWidget(request))


class NicerNamedFileWidget(NamedFileWidget):
    @property
    def allow_nochange(self):
        # Prevent errors caused by missing blob file
        if self.value != self.field.missing_value:
            try:
                blob = getattr(self.value, "_blob", None)
                if blob:
                    blob.__repr__()
            except POSKeyError:
                return False
        return super().allow_nochange

    def extract(self, default=NOVALUE):
        action = self.request.get("%s.action" % self.name, None)
        if action == "remove":
            return None

        value = FileWidget.extract(self, default)

        if value is NOVALUE or (isinstance(value, FileUpload) and not value.filename):
            if self.ignoreContext:
                return default

            dm = getMultiAdapter(
                (
                    self.context,
                    self.field,
                ),
                IDataManager,
            )
            return dm.get()

        # Note that we allow the user to upload an empty file.
        return value


@adapter(INamedFileField, INuPloneFormLayer)
@implementer(IFieldWidget)
def NamedFileWidgetFactory(field, request):
    return FieldWidget(field, NicerNamedFileWidget(request))


class IWysiwygWidget(z3c.form.interfaces.ITextAreaWidget):
    """This is a copy of plone.app.z3cform.wysiwyg.widget.IWysiwygWidget
    from the 4.3 branch.

    Since 4.4 the widget has been removed.
    """

    pass


@implementer_only(IWysiwygWidget)
class WysiwygWidget(z3c.form.browser.textarea.TextAreaWidget):
    """This is a copy of plone.app.z3cform.wysiwyg.widget.WysiwygWidget
    from the 4.3 branch.

    Since 4.4 the widget has been removed.
    """

    klass = "kupu-widget"
    value = ""

    def update(self):
        super(z3c.form.browser.textarea.TextAreaWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)
        # We'll wrap context in the current site *if* it's not already
        # wrapped.  This allows the template to acquire tools with
        # ``context/portal_this`` if context is not wrapped already.
        # Any attempts to satisfy the Kupu template in a less idiotic
        # way failed:
        if getattr(self.form.context, "aq_inner", None) is None:
            self.form.context = Acquisition.ImplicitAcquisitionWrapper(
                self.form.context, getSite()
            )


@adapter(zope.schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@implementer(z3c.form.interfaces.IFieldWidget)
def WysiwygFieldWidget(field, request):
    """This is a copy of plone.app.z3cform.wysiwyg.widget.WysiwygFieldWidget
    from the 4.3 branch.

    Since 4.4 the widget has been removed.
    """
    return z3c.form.widget.FieldWidget(field, WysiwygWidget(request))
