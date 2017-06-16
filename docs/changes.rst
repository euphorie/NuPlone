Changelog
=========

1.5.4 (2017-06-16)
------------------

- Add translation file for Croatioan (hr), currently with one translation

1.5.3 (2017-04-03)
------------------

- Also show the "stupid" div again on text_input, but only if the field
  has a description


1.5.2 (2016-09-29)
------------------

- Streamline File and Image input
- Mostly revert markup change of 1.5.1, since the `<div>` is required
  for making infoBubbles render correctly

1.5.1 (2016-06-20)
------------------

- Fix markup in z3c.form input fields: replace `<div>` around label and input
  with a `<span>` and only show it if it is needed to add dependency classes.

1.5.0 (2015-10-13)
------------------

- Update JS libraries
  jquery from 1.4.4 to 1.11.3
  jquery.ui from 1.8 to 1.11.4
  Add jquery.browser (which adds functionality removed from jquery core)

- Include the new JS libraries and update code to handle them.
  Specifically, the .live method is no longer available and .on must be used.

1.4.5 (2014-08-29)
------------------

- On the PW reset form, catch errors caused by wrong user name and show
  meaningful error message instead of 'Ooops'
- fixed Italian translation for button_cancel (was the same as button_delete),
  OSHA ref #10522

1.4.4 (2014-08-11)
------------------

- Add support for Plone 4.3.3.

1.4.3 (2014-07-09)
------------------

- Bugfix. Site Menu dropdown prevents clicking on certain page elements. (OSHA #10390)
- Bugfix. Site Menu dropdowns truncated in IE. (OSHA #10329)


1.4.2 (2014-07-07)
------------------

- Revert IE 11 CSS fix, has unintented consequences.


1.4.1 (2014-07-07)
------------------

- Update a translation in IT
- CSS fix for IE 11.

1.4.0 - January 9, 2014
-----------------------

- Add an API to the analytics tile to trigger extra (virtual) page views.

- Change analyatics tile to send the authentication status (*anonymous* or
  *authenticated* instead of the users login name.


1.3.9 - January 3, 2014
-----------------------

- Add prototype page for osha library page.


1.3.8 - December 19, 2013
-------------------------

- Fix comaptibility with Chameleon 1.14.

- New translation: Maltese (MT)


1.3.7 - December 12, 2013
-------------------------

- New translations: Italian (IT) and Icelandic (IS)

- Fixed issue with file browse button

- Setup accordian for prototype settings page.


1.3.6 - October 7, 2013
-----------------------

- Modify internal buildout to use the latets buildout and Pillow releases.

- Remove stray space in readonly-attribute for named file widgets. This caused
  IE to treat all file widgets as read-only.


1.3.5 - July 5, 2013
--------------------

- Changed 2 strings in the Greek translation [pyailor]


1.3.4 - July 3, 2013
--------------------

- Enable 'depends' form directive also for schema extended fields.
  [jcbrand]


1.3.3 - April 23, 2013
----------------------

- Added translation to Hungarian
  [pysailor]

- Textual corrections for Lithuanian
  [pysailor]


1.3.2 - April 4, 2013
---------------------

- Add standard makefile to manage builds and cleanup buildout configuration.

- Fix editing of fields using object widgets: their data was not correctly
  extracted due to a missing hidden form field.


1.3.1 - March 6, 2013
---------------------

- Fix a syntax error in template for the select form widget.


1.3 - February 14, 2013 
-----------------------

- Prevent the *Paste* action from being show in places where paste was
  not allowed.

- Stop the portlet sidebar from jumping from left to right on page lods.

- Tighten lxml dependency to make sure security improvements in its html
  cleaner are included.

- Update form markup to add an `error` class on labels for fields with
  errors.

- Add new translations: Finnish and Lithuanian


1.2 - December 7, 2012
----------------------

- Rewrite code to handle links in rich text fields. This fixes ticket
  `ticket 56 <https://github.com/euphorie/Euphorie/issues/56>`_.

- Add new translation: Bulgarian, Flemish, Catalan, Latvian and Portugese.

- Update htmllaundry to 2.0.

- Update TinyMCE to version 3.5.6.

- Configure HTML cleanup code to strip data: attributes. 


1.1 - December 20, 2011
-----------------------

- Allow anonymous users to switch the current language as well. This fixes
  Euphorie ticket `27 <https://github.com/euphorie/Euphorie/issues/27>`_,


1.0.1 - December 9, 2011
------------------------

- Update package metadata.
  [wichert]

- Fix MANIFEST so tiny_mce is included in the distribution.
  [wichert]


1.0 - December 8, 2011
----------------------

- Add support for Plone 4.1 and Chameleon 2.x.
  [wichert]

- Register screen-ie6.css as zrt-resource.
  [jcbrand]

- New Spanish, Czech, Slovenian translations
  [thomas_w]

- Refactored infoPanels on z3cforms to fix alignment issues.
  [jcbrand]

- Don't capitalize questions and legends.
  [jcbrand]

- Add css class to enable secondary InfoPanels (per field).
  [jcbrand]

- Two newlines TinyMCE bug fixed (Github issue #1)
  [jcbrand]


1.0rc8 - May 17, 2011
---------------------

- Correct htmllaundry dependency.
  [wichert]

- Correct location of toolbar CSS.
  [wichert]


1.0rc7 - April 26, 2011
-----------------------

- Exclude prototype from all distribution forms; the symlinked files confuse
  distutils too much.
  [wichert]

- Add MANIFEST.in and restructure symlinks for css/javacsript files to
  guarantee all files are included in eggs.
  [wichert]

1.0rc6 - April 21, 2011
-----------------------

- Re-release rc5 as rc6 to fixup error in source control tagging.
  [wichert]


1.0rc5 - April 21, 2011
-----------------------

- Prefer `Title` method to get the current title for the title of the delete
  confirmation page.
  [wichert]

- Do not put a <p> element in an <object>; IE9 will move it outside the object
  element, thus resulting in leftovers even when using the object->iframe
  conversion.
  [wichert]

- Enable the iframe workaround for IE 9 as well.
  [wichert]

- Add support for status messages containing markup.
  [jcbrand]

- Bugfix. Prevent clicking on the "Actions" site menu action if it doesn't have
  a URL to go to. 
  [jcbrand]


1.0rc4 - Febuary 1, 2011
------------------------

- Paper brown bag: fix initialisation of rich text editor in forms. This
  broke in 1.0rc3 as a part of the tooltip changes.
  [wichert]


1.0rc3 - January 25, 2011
-------------------------

- Upgrade to jQuery 1.4.4 and jQuery UI 1.8.9.
  [wichert]

- Add javascript workaround for bad handling if ``<button>`` elements in
  Internet Explorer versions before 8.
  [wichert]

- Do form-related markup transforms earlier so positioning of tooltips
  from global transforms works correctly.
  [wichert]


1.0rc2 - Janary 11, 2011
------------------------

- Fix TinyMCE: making text bold or italic works again.
  [wichert]

- Expose date/time format methods from the Tools view directly as well
  for use in python code.
  [wichert]


1.0rc1 - December 7, 2010
-------------------------

- zope.i18n is not capable of rendering pre-1900 dates. To prevent site errors
  detect this and return an textual error instead. 
  [wichert]

- Do not load the TinyMCE linesfield plugin. It is not needed, and it triggered
  a symlink handling bug in setuptools/distutils.
  [wichert]

- Fix transparent background for sitemenu in IE7.
  [wichert]

- Refactor positioning of form tooltips.
  [wichert]

- Update to jQuery 1.4.3 and jQuery UI 1.8.6.
  [wichert]


1.0b4 - October 6, 2010
-----------------------

- Update IE8 styling.
  [cornae]

1.0b3 - October 5, 2010
-----------------------

- Correct font reference for IE6 and IE7.
  [wichert]

- Update form field dependency checker to deal with z3c.form's madness of
  always using :list for checkbox field names.
  [wichert]


1.0b2 - September 29, 2010
--------------------------

- Form CSS improvements.
  [cornae]


1.0b1 - September 23, 2010
--------------------------

- Modify site menu to generate the contents of the actions menu in code. This
  makes it easier to extend the menu using a derived class.
  [wichert]

- Make the email address and name of the contact person where emails are send
  to configurable via appconfig.
  [wichert]

- Move ``dfn`` elements for tooltips outside ``label`` elements to make sure
  we can handle click events for them. Otherwise browsers pretend the click
  was targeted to the input element inside the label.
  [cornae, wichert]


1.0a2 - September 9, 2010
-------------------------

- Update error page handler to deal with double acquisition wrapping which
  can happen on certain NotFound errors in Zope 2.12.
  [wichert]

- Add `plone.app.testing <http://pypi.python.org/pypi/plone.app.testing>`_
  based test fixture.
  [wichert]

- Delete some old copy/paste leftovers from `Euphorie
  <http://pypi.python.org/pypi/Euphorie>`_.
  [wichert]


1.0a1 - August 31, 2010
-----------------------

- First release.
  [wichert, cornae]

