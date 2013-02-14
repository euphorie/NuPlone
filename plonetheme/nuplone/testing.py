from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
import plonetheme.nuplone

FIXTURE = PloneWithPackageLayer(
        zcml_filename="configure.zcml",
        zcml_package=plonetheme.nuplone,
        gs_profile_id="plonetheme.nuplone:default",
        name="plonetheme.nuplone:fixture")

NUPLONE_INTEGRATION_TESTING = IntegrationTesting(
        bases=(FIXTURE,), name="NuPlone:Integration")
NUPLONE_FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(FIXTURE,), name="NuPlone:Functional")


__all__ = ['NUPLONE_INTEGRATION_TESTING', 'NUPLONE_FUNCTIONAL_TESTING']
