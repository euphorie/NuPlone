import re
from chameleon.codegen import template
from chameleon.astutil import Symbol
from chameleon.tales import StringExpr
from plonetheme.nuplone.utils import checkPermission


class PermissionExpr(StringExpr):
    def __call__(self, target, engine):
        assignment = super(PermissionExpr, self).__call__(target, engine)
        return assignment + template(
                'target = check_permission(context, target)',
                target=target, check_permission=Symbol(checkPermission))


import five.pt.engine
five.pt.engine.Program.secure_expression_types['permission'] = PermissionExpr
five.pt.engine.Program.expression_types['permission'] = PermissionExpr
