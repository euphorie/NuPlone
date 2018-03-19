# -*- coding: UTF-8 -*-
""" StatusMessage adapter tests.
"""
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.testing import NUPLONE_INTEGRATION_TESTING
from Products.statusmessages.interfaces import IStatusMessage
from unittest import TestCase
from webhelpers.html.builder import literal
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import directlyProvides
from zope.publisher.base import RequestDataMapper
from zope.publisher.base import RequestDataProperty
from zope.publisher.browser import TestRequest as TestRequestBase


class CookieMapper(RequestDataMapper):
    _mapname = '_cookies'

    def __setitem__(self, key, value):
        pass


class TestRequest(TestRequestBase):
    """Zope 3's TestRequest doesn't support item assignment, but Zope 2's
    request does.
    """

    def __setitem__(self, key, value):
        pass

    cookies = RequestDataProperty(CookieMapper)


class TestHTMLStatusMessages(TestCase):
    layer = NUPLONE_INTEGRATION_TESTING

    def testAdapter(self):
        """ Test status messages
            First some boilerplate.
        """
        request = self.request = TestRequest()

        directlyProvides(request, NuPloneSkin)

        # Now lets make sure we can actually adapt the request.
        status = IStatusMessage(self.request)
        self.assertEquals(IStatusMessage.providedBy(status), True)
        assert (hasattr(status, 'addHTMLStatusMessage'))

        # We also need the request to be annotatable:
        directlyProvides(self.request, IAttributeAnnotatable)

        # Make sure there's no stored message.
        self.assertEquals(len(status.show()), 0)

        # Add one message
        status.add(u'test', type=u'info')

        # Now check the results
        messages = status.show()
        self.assertEquals(len(messages), 1)
        self.assertEquals(messages[0].message, u'test')
        self.assertEquals(messages[0].type, u'info')

        # Make sure messages are removed
        self.assertEquals(len(status.show()), 0)

        # Since we accessed the message prior to publishing the page, we must
        # ensure that the messages have been removed from the cookies
        self.assertEquals(len(status.show()), 0)

        # Now we repeat the test, only this time we publish the page prior to
        # retrieving the messages

        # Add one message
        status.add(u'test', type=u'info')

        # Now check the results
        messages = status.show()
        self.assertEqual(len(messages), 1)
        self.assertEquals(messages[0].message, u'test')
        self.assertEquals(messages[0].type, u'info')

        # Make sure messages are removed
        self.assertEquals(len(status.show()), 0)

        # Add two messages
        status.add(u'test', type=u'info')
        status.add(u'test1', u'warn')

        # And check the results again
        messages = status.show()
        self.assertEquals(len(messages), 2)
        test = messages[1]
        self.assertEquals(test.message, u'test1')
        self.assertEquals(test.type, u'warn')

        # Make sure messages are removed again
        self.assertEquals(len(status.show()), 0)

        # Add two identical messages
        status.add(u'test', type=u'info')
        status.add(u'test', type=u'info')

        # And check the results again
        messages = status.show()
        self.assertEquals(len(messages), 1)
        test = messages[0]
        self.assertEquals(test.message, u'test')
        self.assertEquals(test.type, u'info')

        # Make sure messages are removed again
        self.assertEquals(len(status.show()), 0)

        # Test incredibly long messages:
        status.add(u'm' * 0x400, type=u't' * 0x20)

        # And check the results again
        messages = status.show()
        self.assertEquals(len(messages), 1)

        test = messages[0]
        assert (test.message == u'm' * 0x3FF)
        assert (test.type == u't' * 0x1F)

        # Add one HTML messages
        status.addHTML(u'test', type=u'success')

        # And check the results again
        messages = status.show()
        self.assertEquals(len(messages), 1)
        test = messages[0]
        self.assertEquals(test.type, u'success')
        self.assertEquals(test.message, u'test')
        self.assertEquals(type(test.message), literal)

        # Add two HTML messages
        status.addHTML(u'test', type=u'info')
        status.addHTML(u'test1', u'warn')

        # And check the results again
        messages = status.show()
        self.assertEquals(len(messages), 2)
        test = messages[1]
        self.assertEquals(test.message, u'test1')
        self.assertEquals(type(test.message), literal)
        self.assertEquals(test.type, u'warn')

        # add two identical messages
        status.addHTML(u'test', type=u'info')
        status.addHTML(u'test', type=u'info')

        # And check the results again
        messages = status.show()
        self.assertEquals(len(messages), 1)
        test = messages[0]
        self.assertEquals(test.message, u'test')
        self.assertEquals(type(test.message), literal)
        self.assertEquals(test.type, u'info')

        # Make sure messages are removed again
        self.assertEquals(len(status.show()), 0)

        # Test incredibly long messages:
        status.addHTML(u'm' * 0x400, type=u't' * 0x20)

        # And check the results again
        messages = status.show()
        self.assertEquals(len(messages), 1)

        test = messages[0]
        self.assertEquals(type(test.message), literal)
        assert (test.message == '%s' % (u'm' * 0x3FF))
        assert (test.type == u't' * 0x1F)

        # Add two mixed messages
        status.add(u'test', type=u'info')
        status.addHTML(u'test1', u'warn')

        # And check the results again
        messages = status.show()
        self.assertEquals(len(messages), 2)
        test = messages[0]
        self.assertEquals(test.message, u'test')
        self.assertNotEquals(type(test.message), literal)
        self.assertEquals(test.type, u'info')

        test = messages[1]
        self.assertEquals(test.message, u'test1')
        self.assertEquals(type(test.message), literal)
        self.assertEquals(test.type, u'warn')

        # Add a more complicated html message
        status.addHTML(
            u'You can go <a href="http://plone.org">here</a>.',
            type=u'success'
        )
        messages = status.show()
        self.assertEquals(len(messages), 1)
        test = messages[0]
        self.assertEquals(test.type, u'success')
        self.assertEquals(
            test.message,
            u'You can go <a href="http://plone.org" rel="nofollow" target="_blank">here</a>.'  # noqa: E501
        )
        self.assertEquals(type(test.message), literal)

        # Add html message with disallowed tags
        status.addHTML(
            u'<p>You can go <a href="http://plone.org">here</a>.</p>',
            type=u'success'
        )
        messages = status.show()
        self.assertEquals(len(messages), 1)
        test = messages[0]
        self.assertEquals(test.type, u'success')
        self.assertEquals(
            test.message,
            u'You can go <a href="http://plone.org" rel="nofollow" target="_blank">here</a>.'  # noqa: E501
        )
        self.assertEquals(type(test.message), literal)

        status.addHTML(
            u"<script type=\"javascript\">alert('hello')</script>",
            type=u'success'
        )
        messages = status.show()
        self.assertEquals(len(messages), 1)
        test = messages[0]
        self.assertEquals(test.type, u'success')
        self.assertEquals(test.message, '')
        self.assertEquals(type(test.message), literal)

        status.addHTML(
            u'<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgidGVzdCIpOzwvc2NyaXB0Pg==">click me</a>',  # noqa: E501
            type=u'success'
        )
        messages = status.show()
        self.assertEquals(len(messages), 1)
        test = messages[0]
        self.assertEquals(test.type, u'success')
        self.assertEquals(test.message, '<a href="">click me</a>')
        self.assertEquals(type(test.message), literal)
