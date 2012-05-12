from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class CollectiveConference(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.conference
        xmlconfig.file('configure.zcml',
                       collective.conference,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.conference:default')

COLLECTIVE_CONFERENCE_FIXTURE = CollectiveConference()
COLLECTIVE_CONFERENCE_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(COLLECTIVE_CONFERENCE_FIXTURE, ),
                       name="CollectiveConference:Integration")