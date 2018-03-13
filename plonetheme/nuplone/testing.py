# coding=utf-8
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer

import plonetheme.nuplone


FIXTURE = PloneWithPackageLayer(
    zcml_filename="configure.zcml",
    zcml_package=plonetheme.nuplone,
    gs_profile_id="plonetheme.nuplone:default",
    name="plonetheme.nuplone:fixture"
)

NUPLONE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE, ), name="NuPlone:Integration"
)


NUPLONE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, ), name="NuPlone:Functional"
)


NUPLONE_FUNCTIONAL_WITH_PAC_TESTING = FunctionalTesting(
    bases=(
        PLONE_APP_CONTENTTYPES_FIXTURE,
        FIXTURE,
    ),
    name="NuPlone:FunctionalWithPAC",
)


__all__ = ['NUPLONE_INTEGRATION_TESTING', 'NUPLONE_FUNCTIONAL_TESTING']
