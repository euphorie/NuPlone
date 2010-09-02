from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

class NuPloneFixture(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        from zope.configuration import xmlconfig
        import plonetheme.nuplone
        xmlconfig.file("configure.zcml", plonetheme.nuplone, context=configurationContext)

    def setupPloneSite(self, portal):
        from plone.app.testing import applyProfile
        applyProfile(portal, "plonetheme.nuplone:default")

NUPLONE_FIXTURE = NuPloneFixture()
NUPLONE_INTEGRATION_TESTING = IntegrationTesting(bases=(NUPLONE_FIXTURE,), name="NuPlone:Integration")
NUPLONE_FUNCTIONAL_TESTING = FunctionalTesting(bases=(NUPLONE_FIXTURE,), name="NuPlone:Functional")


