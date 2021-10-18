Introduction
============


.. image:: https://github.com/euphorie/NuPlone/workflows/tests/badge.svg
    :target: https://github.com/euphorie/NuPlone/actions?query=workflow%3Atests


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
between this package and the old `NuPlone <http://pypi.python.org/pypi/Products.NuPlone>`_ plone theme.


Compatibility
=============

NuPlone 2.x is meant to be used with Plone 5.2.

Upgrade to NuPlone 2.x
----------------------

NuPlone 2.x no longer uses:
 - ``z3c.appconfig``.
 - ``z3c.zrtresource``
 - the grok ecosystem

The configuration is now stored in the registry:

- instead of ``appconfig["site"]["contact.email"]``, please use the registry record ``plone.email_from_address``.
- instead of ``appconfig["site"]["contact.name"]``, please use the registry record ``plone.email_from_name``.
- instead of ``appconfig["site"]["title"]``, please use the registry record ``plone.site_title``.
- instead of ``appconfig["tile:$TILE_ID"]``, please use the registry record ``plonetheme.nuplone.appconfigtile_$TILE_ID`` (they are expected to contain json).
