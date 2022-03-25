from pkg_resources import get_distribution
from plone.memoize import forever
from Products.Five import BrowserView


class NuPloneVersionView(BrowserView):
    """Helper view to return the NuPlone version. Can be used to break caching
    for resources, like:

    oira.cms.min.js?v=${here/@@nuplone-version}
    """

    @forever.memoize
    def __call__(self):
        return get_distribution("NuPlone").version
