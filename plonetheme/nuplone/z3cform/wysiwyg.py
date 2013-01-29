from zope.interface import Interface
from zope import schema
from five import grok
from plone.directives import form
from plonetheme.nuplone import MessageFactory as _

grok.templatedir("templates")

class ExternalLinkSchema(form.Schema):
    URL = schema.URI(
            title=_("label_url", default=u"URL"),
            required=True)

    title = schema.TextLine(
            title=_("label_title", default=u"Title"),
            required=False)

    new_window = schema.Bool(
            title=_("label_new_window", default=u"Open link in new window"),
            default=True)


class EditLink(form.SchemaForm):
    grok.context(Interface)
    grok.require("cmf.ModifyPortalContent")
    grok.name("edit-link.html")
    grok.template("editlink")

    ignoreContext = True
    schema = ExternalLinkSchema
