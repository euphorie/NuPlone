from Acquisition import aq_inner
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plonetheme.nuplone import MessageFactory as _
from plonetheme.nuplone.utils import createEmailTo
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PasswordResetTool import ExpiredRequestError
from Products.CMFPlone.PasswordResetTool import InvalidRequestError
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MailHost.MailHost import MailHostError
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import form
from z3c.form.button import buttonAndHandler
from zope import schema
from zope.i18n import translate

import logging


log = logging.getLogger(__name__)


class IRequestPasswordReset(model.Schema):
    login = schema.TextLine(title=_("label_login", default="Login"), required=True)


class IPasswordReset(model.Schema):
    login = schema.TextLine(title=_("label_login", default="Login"), required=True)

    password = schema.Password(
        title=_("label_password", default="Password"), required=True
    )


class RequestPasswordForm(AutoExtensibleForm, form.Form):
    email_template = ViewPageTemplateFile("templates/pwreset-email.pt")

    ignoreContext = True
    schema = IRequestPasswordReset
    label = _("header_password_reset_request", default="Reset password")
    default_fieldset_label = None
    description = _(
        "intro_password_reset_request",
        default="For security reasons, we store your password encrypted, "
        "and cannot mail it to you. If you would like to reset "
        "your password, fill out the form below and we will send "
        "you an email at the address you gave when you registered "
        "to start the process of resetting your password.",
    )

    @property
    def email_from_name(self):
        return api.portal.get_registry_record("plone.email_from_name")

    @property
    def email_from_address(self):
        return api.portal.get_registry_record("plone.email_from_address")

    @buttonAndHandler(_("button_send", default="Send"), name="send")
    def handleSend(self, action):
        flash = IStatusMessage(self.request).addStatusMessage
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        pas = getToolByName(self.context, "acl_users")
        mt = getToolByName(self.context, "portal_membership")
        user = pas.getUser(data["login"])
        if user is None:
            log.info("Password reset request for unknown user %s" % data["login"])
            flash(_("error_pwreset_unknown_user", default="Unknown username."), "error")
            return

        member = mt.getMemberById(user.getId())
        email_address = member.getProperty("email")
        if not email_address:
            flash(
                _(
                    "error_pwreset_no_email",
                    default="No known email address for this user.",
                ),
                "error",
            )
            return

        ppr = getToolByName(self.context, "portal_password_reset")
        reset = ppr.requestReset(user.getId())
        portal_url = aq_inner(self.context).absolute_url()
        reset_url = "{}/@@reset-password/{}".format(portal_url, reset["randomstring"])

        data["site"] = self.context.title
        subject = _(
            "password_reset_subject",
            default="Password reset for ${site}",
            mapping=data,
        )
        subject = translate(subject, context=self.request)
        body = self.email_template(
            reset_url=reset_url, login=data["login"], site=self.context.title
        )

        email = createEmailTo(
            self.email_from_name,
            self.email_from_address,
            None,
            email_address,
            subject,
            body,
        )

        mh = getToolByName(self.context, "MailHost")
        try:
            mh.send(email)
        except MailHostError as e:
            log.error(
                "MailHost error sending password reset form to %s: %s", email_address, e
            )
            flash(
                _(
                    "error_contactmail",
                    "An error occured while processing your contact request. Please try again later.",  # noqa: E501
                ),
                "error",
            )
            return
        except OSError as e:
            log.error(
                "Socket error sending password reset form to: %s", email_address, e[1]
            )
            flash(
                _(
                    "error_contactmail",
                    "An error occured while processing your contact request. Please try again later.",  # noqa: E501
                ),
                "error",
            )
            return

        flash(
            _(
                "info_pwrest_mail_sent",
                default="An email with instructions for resetting your password has been sent.",  # noqa: E501
            ),
            "success",
        )
        self.request.response.redirect(portal_url)


class PasswordReset(AutoExtensibleForm, form.Form):
    randomstring = None

    ignoreContext = True
    schema = IPasswordReset
    label = _("header_password_reset", default="Reset password")
    description = _(
        "intro_password_reset",
        default="Please fill out the form below to set your password.",
    )
    default_fieldset_label = None

    def publishTraverse(self, request, name):
        if self.randomstring is not None:
            raise KeyError(name)

        ppr = getToolByName(self.context, "portal_password_reset")
        try:
            ppr.verifyKey(name)
        except (InvalidRequestError, ExpiredRequestError):
            raise KeyError(name)

        self.randomstring = name
        return self

    @buttonAndHandler(_("button_change", default="Change"), name="change")
    def handleChange(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        flash = IStatusMessage(self.request).addStatusMessage
        pas = getToolByName(self.context, "acl_users")
        ppr = getToolByName(self.context, "portal_password_reset")
        user = pas.getUser(data["login"])
        if user is None:
            flash(
                _(
                    "user_name_wrong",
                    "The login name you have provided does not match the username from the password-reset email. Please check your spelling.",  # noqa: E501
                ),
                "error",
            )
            return
        try:
            ppr.resetPassword(user.getId(), self.randomstring, data["password"])
        except InvalidRequestError:
            flash(
                _(
                    "user_name_wrong",
                    "The login name you have provided does not match the username from the password-reset email. Please check your spelling.",  # noqa: E501
                ),
                "error",
            )
            return

        flash(_("password_reset", "Your password has been reset."), "success")
        portal_url = aq_inner(self.context).absolute_url()
        self.request.response.redirect("%s/@@login" % portal_url)
