"""Class: MemberapprovalPlugin
"""

from zope.interface import implements
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

from pas.plugins.memberapproval.interfaces import IMemberapprovalPlugin

class MemberapprovalPlugin(BasePlugin):
    """Multi-plugin

    """
    implements(IMemberapprovalPlugin)
    meta_type = 'memberapproval Plugin'
    security = ClassSecurityInfo()

    def __init__( self, id, title=None ):
        self._setId( id )
        self.title = title

    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials( credentials ):
        login = credentials.get('login')
        password = credentials.get('password')

        if not login or not password:
            return None


InitializeClass( MemberapprovalPlugin )
