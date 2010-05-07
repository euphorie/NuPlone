from zope.interface import Interface
from zope import schema
from five import grok
from plone.directives import form

grok.templatedir("templates")

class ExternalLinkSchema(form.Schema):
    URL = schema.URI(
            title=u"URL",
            required=True)

    title = schema.TextLine(
            title=u"Title",
            required=False)

    new_window = schema.Bool(
            title=u"Open link in new window",
            default=True)


class EditLink(form.SchemaForm):
    grok.context(Interface)
    grok.require("cmf.ModifyPortalContent")
    grok.name("edit-link")
    grok.template("editlink")

    ignoreContext = True
    schema = ExternalLinkSchema
