from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class NuPloneSkin(IDefaultBrowserLayer, INuPloneFormLayer):
    pass
