Changelog
=========

1.0b4 - October 6, 2010
-----------------------

* Update IE8 styling.
  [cornae]

1.0b3 - October 5, 2010
-----------------------

* Correct font reference for IE6 and IE7.
  [wichert]

* Update form field dependency checker to deal with z3c.form's madness of
  always using :list for checkbox field names.
  [wichert]


1.0b2 - September 29, 2010
--------------------------

* Form CSS improvements.
  [cornae]


1.0b1 - September 23, 2010
--------------------------

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

