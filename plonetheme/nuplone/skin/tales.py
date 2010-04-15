import logging
import re
from AccessControl import getSecurityManager
from chameleon.zpt.expressions import ExpressionTranslator
from chameleon.zpt.interfaces import IExpressionTranslator
from chameleon.core import types
from zope.interface import implements

log = logging.getLogger(__name__)


def _checkPermission(context, permission):
    return getSecurityManager().checkPermission(permission, context)


class PermissionTranslator(ExpressionTranslator):
    implements(IExpressionTranslator)

    symbol = "_checkPermission"
    re_name = re.compile(r"^[a-z]+$")

    def translate(self, string, escape=None):
        if not string:
            return None
        string=string.strip()
        if self.re_name.match(string) is None:
            raise SyntaxError(string)
        value=types.value("%s(context, '%s')" % (self.symbol, string))
        value.symbol_mapping[self.symbol]=_checkPermission
        return value


