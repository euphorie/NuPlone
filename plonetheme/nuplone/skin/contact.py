import logging
import socket
from Acquisition import aq_inner
from zope import schema
from five import grok
from zope.i18n import translate
from zope.component import queryUtility
from plone.directives import form
from plonetheme.nuplone import MessageFactory as _
from Products.MailHost.MailHost import MailHostError
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form.button import buttonAndHandler
from z3c.appconfig.interfaces import IAppConfig
from plonetheme.nuplone.z3cform.form import FieldWidgetFactory
from plonetheme.nuplone.utils import createEmailTo

log = logging.getLogger(__name__)

TextSpan7 = FieldWidgetFactory("z3c.form.browser.text.TextFieldWidget", klass="span-7")
TextLines4Rows = FieldWidgetFactory("z3c.form.browser.textlines.TextLinesFieldWidget", rows=4)


class IContact(form.Schema):
    name = schema.TextLine(
            title=_(u"label_your_name", default="Your name"),
            required=True)
    form.widget(name="plonetheme.nuplone.skin.contact.TextSpan7")

    email = schema.ASCIILine(
            title=_("label_email", default="Email address"),
            required=True)
    form.widget(email="plonetheme.nuplone.skin.contact.TextSpan7")

    subject = schema.TextLine(
            title=_(u"label_subject", default=u"Subject"),
            required=True)
    form.widget(subject="plonetheme.nuplone.skin.contact.TextSpan7")

    message = schema.Text(
            title=_("label_contact_text", default="Your message"),
            required=True)
    form.widget(message="plonetheme.nuplone.skin.contact.TextLines4Rows")



class ContactForm(form.SchemaForm):
    grok.context(ISiteRoot)
    grok.name("contact")
    grok.require("zope2.Public")

    ignoreContext = True
    schema = IContact
    label = _(u"header_contact", default="Contact")
    default_fieldset_label = None

    @buttonAndHandler(_("button_send", default="Send"), name="send")
    def handleSend(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        appconfig = queryUtility(IAppConfig) or {}
        siteconfig = appconfig.get("site", {})

        subject=_(u"contact_mail_subject", default=u"Contact request: ${subject}", mapping=data)
        subject=translate(subject, context=self.request)

        email=createEmailTo(data["name"], data["email"],
                            siteconfig.get("contact.name", self.context.email_from_name),
                            siteconfig.get("contact.email", self.context.email_from_address),
                            subject,
                            data["message"])
        mh=getToolByName(self.context, "MailHost")
        flash=IStatusMessage(self.request).addStatusMessage
        try:
            mh.send(email)
        except MailHostError, e:
            log.error("MailHost error sending contact form for %s: %s", data["email"], e)
            flash(_(u"error_contactmail", u"An error occured while processing your contact request. Please try again later."), "error")
            return
        except socket.error, e:
            log.error("Socket error sending contact form for %s: %s", data["email"], e[1])
            flash(_(u"error_contactmail", u"An error occured while processing your contact request. Please try again later."), "error")
            return

        flash(_(u"Message sent"), "success")
        self.request.response.redirect(aq_inner(self.context).absolute_url())

