import unittest2 as unittest

from zExceptions import Unauthorized

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from collective.conference.track import ITrack


from collective.conference.testing import\
    COLLECTIVE_CONFERENCE_INTEGRATION_TESTING


class TestTrackIntegration(unittest.TestCase):

    layer = COLLECTIVE_CONFERENCE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_adding(self):

        # We can't add this directly
        try:
            self.folder.invokeFactory('collective.conference.trackk', 'track1')
            self.fail('Conference tracks should not be addable except within conference programs.')
        except (ValueError, Unauthorized):
            pass

        self.folder.invokeFactory('collective.conference.program', 'program1')
        p1 = self.folder['program1']

        p1.invokeFactory('collective.conference.track', 'track1')
        s1 = p1['track1']
        self.failUnless(ITrack.providedBy(s1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.conference.track')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.conference.track')
        schema = fti.lookupSchema()
        self.assertEquals(ITrack, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.conference.track')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(ITrack.providedBy(new_object))

    def test_catalog_index_metadata(self):
        self.failUnless('track' in self.portal.portal_catalog.indexes())
        self.failUnless('track' in self.portal.portal_catalog.schema())

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
