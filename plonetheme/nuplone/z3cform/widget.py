from zope.component import adapter
from zope.interface import implementer

from zope.schema.interfaces import IChoice
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from plonetheme.nuplone.z3cform.utils import getVocabulary
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from z3c.form.browser.radio import RadioWidget
from z3c.form.browser.select import SelectWidget

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


