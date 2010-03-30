import os.path
from plone.z3cform.interfaces import IWrappedForm
from plone.z3cform.templates import FormTemplateFactory
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from z3c.form.error import ErrorViewTemplateFactory

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

layout_factory = FormTemplateFactory(
            os.path.join(TEMPLATE_DIR, "wrappedform.pt"),
            form=IWrappedForm,
            request=INuPloneFormLayer)


ErrorViewTemplate = ErrorViewTemplateFactory(os.path.join(TEMPLATE_DIR, "error.pt"))
