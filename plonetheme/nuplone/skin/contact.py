import logging
import socket
from email.MIMEText import MIMEText
from email.Header import Header
import email.utils as emailutils
from Acquisition import aq_inner
from zope import schema
from five import grok
from zope.i18n import translate
from plone.directives import form
from plonetheme.nuplone import MessageFactory as _
from Products.MailHost.MailHost import MailHostError
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form.button import buttonAndHandler

log = logging.getLogger(__name__)

class IContact(form.Schema):
    name = schema.TextLine(
            title=_(u"label_your_name", default="Your name"),
            required=True)

    email = schema.ASCIILine(
            title=_("label_email", default="Email address"),
            required=True)

    subject = schema.TextLine(
            title=_(u"label_subject", default=u"Subject"),
            required=True)

    message = schema.Text(
            title=_("label_contact_text", default="Your message"),
            required=True)


def createEmailTo(sender_name, sender_email, recipient_name, recipient_email,
                  subject, body, format="plain"):
    """Create an :obj:`email.MIMEText.MIMEtext` instance for an email. This
    method will take care of adding addings a date header and message ID
    to the email, as well as quoting of non-ASCII content.
    """
    if isinstance(body, unicode):
        mail=MIMEText(body.encode("utf-8"), format, "utf-8")
    else:
        mail=MIMEText(body, format)

    mail["From"]=emailutils.formataddr((sender_name, sender_email))
    mail["To"]=emailutils.formataddr((recipient_name, recipient_email))
    mail["Subject"]=Header(subject.encode("utf-8"), "utf-8")
    mail["Message-Id"]=emailutils.make_msgid()
    mail["Date"]=emailutils.formatdate(localtime=True)
    mail.set_param("charset", "utf-8")

    return mail


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

        subject=_(u"contact_mail_subject", default=u"Contact request: ${subject}", mapping=data)
        subject=translate(subject, context=self.request)

        email=createEmailTo(data["name"], data["email"],
                            self.context.email_from_name,
                            self.context.email_from_address,
                            subject,
                            data["message"])
        mh=getToolByName(self.context, "MailHost")
        flash=IStatusMessage(self.request).addStatusMessage
        try:
            mh.send(email)
        except MailHostError, e:
            log.error("MailHost error sending contact form for %s: %s", data["email"], e)
            flash(_(u"error_contactmail", u"An error occured while your contact request. Please try again later."), "error")
            return
        except socket.error, e:
            log.error("Socket error sending contact form for s: %s", data["email"], e[1])
            flash(_(u"error_contactmail", u"An error occured while your contact request. Please try again later."), "error")
            return

        flash(_(u"Message sent"), "success")
        self.request.response.redirect(aq_inner(self.context).absolute_url())

