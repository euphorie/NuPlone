Changelog
=========

1.0 - Unreleased
----------------

* Modify site menu to generate the contents of the actions menu in code. This
  makes it easier to extend the menu using a derived class.
  [wichert]

* Make the email address and name of the contact person where emails are send
  to configurable via appconfig.
  [wichert]

* Move ``dfn`` elements for tooltips outside ``label`` elements to make sure
  we can handle click events for them. Otherwise browsers pretend the click
  was targeted to the input element inside the label.
  [cornae, wichert]


1.0a2 - September 9, 2010
-------------------------

* Update error page handler to deal with double acquisition wrapping which
  can happen on certain NotFound errors in Zope 2.12.
  [wichert]

* Add `plone.app.testing <http://pypi.python.org/pypi/plone.app.testing>`_
  based test fixture.
  [wichert]

* Delete some old copy/paste leftovers from `Euphorie
  <http://pypi.python.org/pypi/Euphorie>`_.
  [wichert]


1.0a1 - August 31, 2010
-----------------------

* First release.
  [wichert, cornae]

