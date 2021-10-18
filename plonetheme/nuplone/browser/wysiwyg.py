from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plonetheme.nuplone import MessageFactory as _
from z3c.form import form
from zope import schema


class ExternalLinkSchema(model.Schema):
    URL = schema.URI(title=_("label_url", default=u"URL"), required=True)

    title = schema.TextLine(title=_("label_title", default=u"Title"), required=False)

    new_window = schema.Bool(
        title=_("label_new_window", default=u"Open link in new window"), default=True
    )


class EditLink(AutoExtensibleForm, form.EditForm):

    ignoreContext = True
    schema = ExternalLinkSchema
