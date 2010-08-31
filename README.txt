Introduction
============

This package implements a new user interface for `Plone <http://plone.org/>`_.
The design goals for this user interface are:

* support a single form toolkit well instead of multiple toolkits 
  reasonably well. The chosen form toolkit is `z3c.form
  <http://pypi.python.org/pypi/z3c.form>`_.

* Do not store application configuration in the ZODB, but use simple
  .ini-style textfiles.

* One Zope - one site. No support for multiple sites in a single instance.

* Use tiles everywhere. No viewlets, portlets or other concepts.

* Only support one way to create pages: browser views. CMF skins are
  explicitly not supported.

* Use documented markup patterns to add behaviour to pages. No KSS or
  page-specific javascript.

* Minimal markup, move complexity to standard and documented CSS.



Disclaimer
==========

Although the name of this package may suggest otherwise there is little relation
between this package and the old `NuPlone
<http://pypi.python.org/pypi/Products.NuPlone>`_ plone theme. 

