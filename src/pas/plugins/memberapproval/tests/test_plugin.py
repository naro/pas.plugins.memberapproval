import unittest2 as unittest

from pas.plugins.memberapproval.tests.layer import MEMBERAPPROVAL_INTEGRATION_TESTING
from pas.plugins.memberapproval.install import manage_add_memberapproval_plugin
from pas.plugins.memberapproval.utils import enablePluginInterfaces, getPAS
from pas.plugins.memberapproval.events import IUserApprovedEvent
from pas.plugins.memberapproval.events import IUserDisapprovedEvent
from pas.plugins.memberapproval.interfaces import IMemberApprovalPlugin
from plone.app.testing import TEST_USER_ROLES

USER_ID = 'user_1'
USER_NAME = 'user'
USER_PASSWORD = 'secret'

class PluginUnitTest(unittest.TestCase):

    def testOne(self):
        self.assertEqual(1,1)

class PluginTest(unittest.TestCase):
    
    layer = MEMBERAPPROVAL_INTEGRATION_TESTING
    
    def setUp(self):
        self.portal = self.layer['portal']
        manage_add_memberapproval_plugin(self.portal.acl_users, "source_users_approval")
        enablePluginInterfaces()
        self.plugin = self.portal.acl_users.source_users_approval
        self.plugin.addUser(
                USER_ID,
                USER_NAME,
                USER_PASSWORD)
        for role in TEST_USER_ROLES:
            self.portal.acl_users.portal_role_manager.doAssignRoleToPrincipal(USER_ID, role)
        
    def testInstalled(self):
        pas = getPAS()
        self.failUnless('source_users' in pas.objectIds())

    def testLogin(self):
        self.plugin.unapproveUser(USER_ID)
        r = self.plugin.authenticateCredentials(dict(
            login=USER_ID,
            password = USER_PASSWORD
        ))
        self.failIf(r is not None)
        
    def testApproved(self):
        self.plugin.approveUser(USER_ID)
        r = self.plugin.authenticateCredentials(dict(
            login=USER_ID,
            password = USER_PASSWORD
        ))
        self.failIf(r is None)

    def testEnumerate(self):
        # 2 users total = TEST_USER and USER created in setUp
        self.assertEqual(len(self.plugin.enumerateUsers()), 2)

        # No approval query - return all
        self.plugin.unapproveUser(USER_ID)
        self.assertEqual(len(self.plugin.enumerateUsers()), 2)

        # Only approved
        r = self.plugin.enumerateUsers(approved=True)
        self.assertEqual(len(r), 0)
        
        self.plugin.approveUser(USER_ID)
        r = self.plugin.enumerateUsers(approved=True)
        self.assertEqual(len(r), 1)

        r = self.plugin.enumerateUsers(approved=False)
        self.assertEqual(len(r), 1)
        
        self.plugin.unapproveUser(USER_ID)
        r = self.plugin.enumerateUsers(approved=False)
        self.assertEqual(len(r), 2)

    def test_plugin_registered(self):
        plugins = self.portal.acl_users['plugins']
        my_plugin_id = self.plugin.getId()
        self.failUnless(my_plugin_id in plugins.listPluginIds(IMemberApprovalPlugin))

    def test_event_approve(self):
        from zope.component import adapter
        from zope.component import getGlobalSiteManager
        @adapter(IUserApprovedEvent)
        def user_approved_handler(event):
            self.assertEqual(event.userid, USER_ID)
            
        self.plugin.unapproveUser(USER_ID)
        gsm = getGlobalSiteManager()
        gsm.registerHandler(user_approved_handler)
        self.plugin.approveUser(USER_ID)
        gsm.unregisterHandler(user_approved_handler)

    def test_event_disapprove(self):
        from zope.component import adapter
        from zope.component import getGlobalSiteManager
        @adapter(IUserDisapprovedEvent)
        def user_disapproved_handler(event):
            self.assertEqual(event.userid, USER_ID)
            
        self.plugin.approveUser(USER_ID)
        gsm = getGlobalSiteManager()
        gsm.registerHandler(user_disapproved_handler)
        self.plugin.unapproveUser(USER_ID)
        gsm.unregisterHandler(user_disapproved_handler)
