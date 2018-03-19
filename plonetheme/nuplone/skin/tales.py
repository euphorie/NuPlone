from chameleon.astutil import Symbol
from chameleon.codegen import template
from chameleon.tales import StringExpr
from plonetheme.nuplone.utils import checkPermission

import five.pt.engine


class PermissionExpr(StringExpr):

    def __call__(self, target, engine):
        assignment = super(PermissionExpr, self).__call__(target, engine)
        return assignment + template(
            'target = check_permission(context, target)',
            target=target,
            check_permission=Symbol(checkPermission)
        )


five.pt.engine.Program.secure_expression_types['permission'] = PermissionExpr
five.pt.engine.Program.expression_types['permission'] = PermissionExpr
