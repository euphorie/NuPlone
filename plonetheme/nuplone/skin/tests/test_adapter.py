# -*- coding: UTF-8 -*-
""" StatusMessage adapter tests.
"""
from plonetheme.nuplone.testing import NUPLONE_INTEGRATION_TESTING
from Products.statusmessages.interfaces import IStatusMessage
from unittest import TestCase

import six


class TestHTMLStatusMessages(TestCase):
    layer = NUPLONE_INTEGRATION_TESTING

    def testAdapter(self):
        """Test status messages
        First some boilerplate.
        """
        request = self.layer["request"].clone()

        # Now lets make sure we can actually adapt the request.
        status = IStatusMessage(request)
        self.assertTrue(IStatusMessage.providedBy(status))

        # Make sure there's no stored message.
        self.assertEqual(len(status.show()), 0)

        # Add one message
        status.add(u"test", type=u"info")

        # Now check the results
        messages = status.show()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, u"test")
        self.assertEqual(messages[0].type, u"info")

        # Make sure messages are removed
        self.assertEqual(len(status.show()), 0)

        # Since we accessed the message prior to publishing the page, we must
        # ensure that the messages have been removed from the cookies
        self.assertEqual(len(status.show()), 0)

        # Now we repeat the test, only this time we publish the page prior to
        # retrieving the messages

        # Add one message
        status.add(u"test", type=u"info")

        # Now check the results
        messages = status.show()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, u"test")
        self.assertEqual(messages[0].type, u"info")

        # Make sure messages are removed
        self.assertEqual(len(status.show()), 0)

        # Add two messages
        status.add(u"test", type=u"info")
        status.add(u"test1", u"warn")

        # And check the results again
        messages = status.show()
        self.assertEqual(len(messages), 2)
        test = messages[1]
        self.assertEqual(test.message, u"test1")
        self.assertEqual(test.type, u"warn")

        # Make sure messages are removed again
        self.assertEqual(len(status.show()), 0)

        # Add two identical messages
        status.add(u"test", type=u"info")
        status.add(u"test", type=u"info")

        # And check the results again
        messages = status.show()
        self.assertEqual(len(messages), 1)
        test = messages[0]
        self.assertEqual(test.message, u"test")
        self.assertEqual(test.type, u"info")

        # Make sure messages are removed again
        self.assertEqual(len(status.show()), 0)

        # Test incredibly long messages:
        status.add(u"m" * 0x400, type=u"t" * 0x20)

        # And check the results again
        messages = status.show()
        self.assertEqual(len(messages), 1)

        test = messages[0]
        assert test.message == u"m" * 0x3FF
        assert test.type == u"t" * 0x1F

        # Add one HTML messages
        status.add(u"test", type=u"success")

        # And check the results again
        messages = status.show()
        self.assertEqual(len(messages), 1)
        test = messages[0]
        self.assertEqual(test.type, u"success")
        self.assertEqual(test.message, u"test")
        self.assertIsInstance(test.message, six.text_type)

        # Add two HTML messages
        status.add(u"test", type=u"info")
        status.add(u"test1", u"warn")

        # And check the results again
        messages = status.show()
        self.assertEqual(len(messages), 2)
        test = messages[1]
        self.assertEqual(test.message, u"test1")
        self.assertIsInstance(test.message, six.text_type)
        self.assertEqual(test.type, u"warn")

        # add two identical messages
        status.add(u"test", type=u"info")
        status.add(u"test", type=u"info")

        # And check the results again
        messages = status.show()
        self.assertEqual(len(messages), 1)
        test = messages[0]
        self.assertEqual(test.message, u"test")
        self.assertIsInstance(test.message, six.text_type)
        self.assertEqual(test.type, u"info")

        # Make sure messages are removed again
        self.assertEqual(len(status.show()), 0)

        # Test incredibly long messages:
        status.add(u"m" * 0x400, type=u"t" * 0x20)

        # And check the results again
        messages = status.show()
        self.assertEqual(len(messages), 1)

        test = messages[0]
        self.assertIsInstance(test.message, six.text_type)
        assert test.message == "%s" % (u"m" * 0x3FF)
        assert test.type == u"t" * 0x1F

        # Add two mixed messages
        status.add(u"test", type=u"info")
        status.add(u"test1", u"warn")

        # And check the results again
        messages = status.show()
        self.assertEqual(len(messages), 2)
        test = messages[0]
        self.assertEqual(test.message, u"test")
        self.assertIsInstance(test.message, six.text_type)
        self.assertEqual(test.type, u"info")

        test = messages[1]
        self.assertEqual(test.message, u"test1")
        self.assertIsInstance(test.message, six.text_type)
        self.assertEqual(test.type, u"warn")

        # Add a more complicated html message
        status.add(u'You can go <a href="http://plone.org">here</a>.', type=u"success")
        messages = status.show()
        self.assertEqual(len(messages), 1)
        test = messages[0]
        self.assertEqual(test.type, u"success")
        self.assertEqual(
            test.message,
            u'You can go <a href="http://plone.org">here</a>.',  # noqa: E501
        )
        self.assertIsInstance(test.message, six.text_type)
