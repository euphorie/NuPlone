import os.path
from z3c.form.interfaces import IForm
from plone.z3cform.interfaces import IFormWrapper
from plone.z3cform.interfaces import IWrappedForm
from plone.z3cform.templates import FormTemplateFactory
from plone.z3cform.templates import ZopeTwoFormTemplateFactory
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from z3c.form.error import ErrorViewTemplateFactory

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

layout_factory = ZopeTwoFormTemplateFactory(
            os.path.join(TEMPLATE_DIR, "layout.pt"),
            form=IFormWrapper, 
            request=INuPloneFormLayer)

wrapped_form_factory = FormTemplateFactory(
            os.path.join(TEMPLATE_DIR, "wrappedform.pt"),
            form=IWrappedForm,
            request=INuPloneFormLayer)

form_factory = ZopeTwoFormTemplateFactory(
            os.path.join(TEMPLATE_DIR, "form.pt"),
            form=IForm,
            request=INuPloneFormLayer)


ErrorViewTemplate = ErrorViewTemplateFactory(os.path.join(TEMPLATE_DIR, "error.pt"))
