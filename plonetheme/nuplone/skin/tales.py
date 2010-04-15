import logging
import re
from AccessControl import getSecurityManager
from zope.component import queryUtility
from chameleon.zpt.expressions import ExpressionTranslator
from chameleon.zpt.interfaces import IExpressionTranslator
from chameleon.core import types
from zope.interface import implements
from zope.security.interfaces import IPermission

log = logging.getLogger(__name__)


def _checkPermission(context, permission):
    title = queryUtility(IPermission, name=permission)
    if title is None:
        title=permission
    return getSecurityManager().checkPermission(title, context)


class PermissionTranslator(ExpressionTranslator):
    implements(IExpressionTranslator)

    symbol = "_checkPermission"
    re_name = re.compile(r"^[A-z _-]+$")

    def translate(self, string, escape=None):
        if not string:
            return None
        string=string.strip()
        if self.re_name.match(string) is None:
            raise SyntaxError(string)
        value=types.value("%s(context, '%s')" % (self.symbol, string))
        value.symbol_mapping[self.symbol]=_checkPermission
        return value


