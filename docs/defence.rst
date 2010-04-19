Why reimplement instead of reuse?
---------------------------------

In several places NuPlone[r] reimplements functionality that already exists
elsewhere in the Plone stack. This is done deliberately to create cleaner
and simpler code that is not spread out over multiple packages. An extreme
example of this is the navigation tree: the navigation tree code in Plone is
split over Products.CMFPlone, plone.app.layout and plone.app.portlets. It
involves several adapters, is configurable in at least two different places,
and has more knobs than anyone has ever used. The NuPlone[r] implementation has
no configurable options and is implemented as a single class in under 100 lines
of python.

No default pages
----------------
The concept of default pages has proven to be very confusing for users. Instead
of trying to improve what we consider to be a broken concept NuPlone[r] is based
on the assumption that all contact can act as a folder.

No support for Archetypes/formlib
---------------------------------
Styling forms and views for content types is a lot of hard work. Instead of
trying to to this properly for three different form systems we decided to
only support one, but do that one as well as possible for generated forms. We
decided to support z3c.form on the basis that this is the currently preferred
form toolkit in the Zope world, and used by the up and coming Dexterity content
framework.

One Zope - one site
-------------------
A lot of the complexity in Plone comes from the need to support multiple
differently configured sites within the same Zope instance. We feel that
this is not a valid use case for the target audience for Plone: sites
that require enterprise features such as offered by Plone. Small simple
sites are probably better served by a simpler CMS.

Therefore NuPlone[r] does not support multiple sites within a Zope instance.
Where possible all configuration is managed via simple configuration
files on the filesystem. This simplifies a lot of code, and makes a lot
of zcml, GenericSetup profiles, persistent component registries and other
logic unnnecessary. The result is a simpler and faster Plone.

No main_template
----------------
The markup and CSS for NuPlone[r] is very different than that used by the
common Plone themes. In order to prevent "leaking" of old style markup
into NuPlone[r] we use a different layout template name and different
METAL slot names. We want people to rethink their user interface and
markup as part of a migration to NuPlone[3]


No portlets or viewlets
-----------------------
Plone 3 and 4 have many different ways to customise a page layout: METAL
slots, portlets and viewlets. All of these try to solve the same kind
of problem in different ways, but each with their own restrictions and
implementation choices. The result feels overly complex and hard to manage.
NuPlone[r] only supports a single concept: the tile. Tiles can be inserted
at any part of the page and are configurable using a simple textfile.

