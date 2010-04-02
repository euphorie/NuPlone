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

