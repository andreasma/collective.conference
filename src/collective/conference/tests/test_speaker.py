import unittest2 as unittest

from plone.mocktestcase import MockTestCase

from zope.component import createObject
from zope.component import queryUtility

from zope.app.container.contained import ObjectAddedEvent

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from collective.conference.speaker import ISpeaker
from collective.conference.speaker import notifyUser

from collective.conference.testing import\
    COLLECTIVE_CONFERENCE_INTEGRATION_TESTING


class TestPresenterMock(MockTestCase):

    def test_notify_user(self):

        # dummy speaker
        speaker = self.create_dummy(
                __parent__=None,
                __name__=None,
                title="Jim",
                absolute_url=lambda: 'http://example.org/speaker',
            )

        # dummy event
        event = ObjectAddedEvent(speaker)

        # search result for acl_users
        user_info = [{'email': 'jim@example.org', 'id': 'jim'}]

        # email data
        message = "A speaker called Jim was added here http://example.org/speaker"
        email = "jim@example.org"
        sender = "test@example.org"
        subject = "Is this you?"

        # mock tools/portal

        portal_mock = self.mocker.mock()
        self.expect(portal_mock.getProperty('email_from_address')).result('test@example.org')

        portal_url_mock = self.mocker.mock()
        self.mock_tool(portal_url_mock, 'portal_url')
        self.expect(portal_url_mock.getPortalObject()).result(portal_mock)

        acl_users_mock = self.mocker.mock()
        self.mock_tool(acl_users_mock, 'acl_users')
        self.expect(acl_users_mock.searchUsers(fullname='Jim')).result(user_info)

        mail_host_mock = self.mocker.mock()
        self.mock_tool(mail_host_mock, 'MailHost')
        self.expect(mail_host_mock.secureSend(message, email, sender, subject))

        # put mock framework into replay mode
        self.replay()

        # call the method under test
        notifyUser(speaker, event)

        # we could make additional assertions here, e.g. if the function
        # returned something. The mock framework will verify the assertions
        # about expected call sequences.


class TestPresenterIntegration(unittest.TestCase):

    layer = COLLECTIVE_CONFERENCE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_adding(self):
        self.folder.invokeFactory('collective.conference.speaker', 'speaker1')
        p1 = self.folder['speaker1']
        self.failUnless(ISpeaker.providedBy(p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.conference.speaker')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.conference.speaker')
        schema = fti.lookupSchema()
        self.assertEquals(ISpeaker, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.conference.speaker')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(ISpeaker.providedBy(new_object))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
