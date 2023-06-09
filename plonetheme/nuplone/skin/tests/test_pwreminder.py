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

        # The browser tests was replaced because of this issue:
        # - https://github.com/plone/plone.testing/issues/83
        #
        # browser = Browser(self.layer["app"])
        # browser.handleErrors = False
        # url = "%s/reset-password/bogus" % self.layer["portal"].absolute_url()
        with self.assertRaises(NotFound):
            self.layer["portal"].restrictedTraverse("reset-password/bogus")
            # browser.open(url)

    def testDoubleKeys(self):
        from zExceptions import NotFound

        # The browser tests was replaced because of this issue:
        # - https://github.com/plone/plone.testing/issues/83
        #
        # browser = Browser(self.layer["app"])
        # browser.handleErrors = False
        # url = "%s/reset-password/one/two" % self.layer["portal"].absolute_url()
        with self.assertRaises(NotFound):
            self.layer["portal"].restrictedTraverse("reset-password/one/two")
            # browser.open(url)
