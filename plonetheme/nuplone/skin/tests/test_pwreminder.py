from plone.testing.zope import Browser
from plonetheme.nuplone.testing import NUPLONE_FUNCTIONAL_TESTING

import unittest


class PasswordResetTests(unittest.TestCase):
    layer = NUPLONE_FUNCTIONAL_TESTING

    def testNoKey(self):
        browser = Browser(self.layer["app"])
        browser.open("%s/reset-password" % self.layer["portal"].absolute_url())
        browser.getForm("form").submit()

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
