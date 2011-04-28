import unittest2 as unittest

from pas.plugins.memberapproval.tests.layer import MEMBERAPPROVAL_INTEGRATION_TESTING

class PluginUnitTest(unittest.TestCase):

    def testOne(self):
        self.assertEqual(1,1)

class PluginTest(unittest.TestCase):
    
    layer = MEMBERAPPROVAL_INTEGRATION_TESTING
    
    def setUp(self):
        self.portal = self.layer['portal']
        
    def testOne(self):
        self.assertEqual(1,1)