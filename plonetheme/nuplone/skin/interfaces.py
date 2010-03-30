from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer


class NuPloneSkin(IDefaultBrowserLayer, INuPloneFormLayer):
    pass
