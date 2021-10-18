from Acquisition import aq_inner
from plone import api
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plonetheme.nuplone import MessageFactory as _
from plonetheme.nuplone.utils import createEmailTo
from plonetheme.nuplone.z3cform.form import FieldWidgetFactory
from Products.CMFCore.utils import getToolByName
from Products.MailHost.MailHost import MailHostError
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import form
from z3c.form.button import buttonAndHandler
from zope import schema
from zope.i18n import translate

import logging
import socket


log = logging.getLogger(__name__)

TextSpan7 = FieldWidgetFactory("z3c.form.browser.text.TextFieldWidget", klass="span-7")
TextLines4Rows = FieldWidgetFactory(
    "z3c.form.browser.textlines.TextLinesFieldWidget", rows=4
)


class IContact(model.Schema):
    name = schema.TextLine(
        title=_(u"label_your_name", default="Your name"), required=True
    )
    directives.widget(name="plonetheme.nuplone.browser.contact.TextSpan7")

    email = schema.ASCIILine(
        title=_("label_email", default="Email address"), required=True
    )
    directives.widget(email="plonetheme.nuplone.browser.contact.TextSpan7")

    subject = schema.TextLine(
        title=_(u"label_subject", default=u"Subject"), required=True
    )
    directives.widget(subject="plonetheme.nuplone.browser.contact.TextSpan7")

    message = schema.Text(
        title=_("label_contact_text", default="Your message"), required=True
    )
    directives.widget(message="plonetheme.nuplone.browser.contact.TextLines4Rows")


class ContactForm(AutoExtensibleForm, form.Form):

    ignoreContext = True
    schema = IContact
    label = _(u"header_contact", default="Contact")
    default_fieldset_label = None

    @property
    def email_from_name(self):
        return api.portal.get_registry_record("plone.email_from_name")

    @property
    def email_from_address(self):
        return api.portal.get_registry_record("plone.email_from_address")

    @buttonAndHandler(_("button_send", default="Send"), name="send")
    def handleSend(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        subject = _(
            u"contact_mail_subject",
            default=u"Contact request: ${subject}",
            mapping=data,
        )
        subject = translate(subject, context=self.request)

        email = createEmailTo(
            data["name"],
            data["email"],
            self.email_from_name,
            self.email_from_address,
            subject,
            data["message"],
        )
        mh = getToolByName(self.context, "MailHost")
        flash = IStatusMessage(self.request).addStatusMessage
        try:
            mh.send(email)
        except MailHostError as e:
            log.error(
                "MailHost error sending contact form for %s: %s", data["email"], e
            )
            flash(
                _(
                    u"error_contactmail",
                    u"An error occured while processing your contact request. Please try again later.",  # noqa: E501
                ),
                "error",
            )
            return
        except socket.error as e:
            log.error(
                "Socket error sending contact form for %s: %s", data["email"], e[1]
            )
            flash(
                _(
                    u"error_contactmail",
                    u"An error occured while processing your contact request. Please try again later.",  # noqa: E501
                ),
                "error",
            )
            return

        flash(_(u"Message sent"), "success")
        self.request.response.redirect(aq_inner(self.context).absolute_url())
