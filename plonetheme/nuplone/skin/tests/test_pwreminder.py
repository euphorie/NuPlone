import unittest2 as unittest
from plonetheme.nuplone.testing import NUPLONE_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser


class PasswordResetTests(unittest.TestCase):
    layer = NUPLONE_FUNCTIONAL_TESTING

    # XXX Disabled for now because grok-style views are not working in
    # the plone.app.testing-based setup.
    def XtestNoKey(self):
        browser = Browser(self.layer["app"])
        browser.open("%s/reset-password" % self.layer["portal"].absolute_url())
        browser.getForm().submit()

    def testInvalidKey(self):
        from zExceptions import NotFound
        browser = Browser(self.layer["app"])
        browser.handleErrors = False
        url = "%s/reset-password/bogus" % self.layer["portal"].absolute_url()
        self.assertRaises(NotFound, browser.open, url)

    def testDoubleKeys(self):
        from zExceptions import NotFound
        browser = Browser(self.layer["app"])
        browser.handleErrors = False
        url = "%s/reset-password/one/two" % self.layer["portal"].absolute_url()
        self.assertRaises(NotFound, browser.open, url)
