from collective.lineage.testing import LINEAGE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class LineageRegistry(PloneSandboxLayer):

    defaultBases = (LINEAGE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import lineage.registry
        xmlconfig.file('configure.zcml', lineage.registry,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        self['portal'] = portal

LINEAGEREGISTRY_FIXTURE = LineageRegistry()
LINEAGEREGISTRY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LINEAGEREGISTRY_FIXTURE, ),
    name="lineage.registry:Integration"
)
