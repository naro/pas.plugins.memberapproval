"""Class: MemberapprovalPlugin
"""

import copy
from BTrees.OOBTree import OOBTree
from zope.interface import implements
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.ZODBUserManager import ZODBUserManager
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserAdderPlugin
from Products.PluggableAuthService.utils import createViewName

from pas.plugins.memberapproval.interfaces import IMemberapprovalPlugin

APPROVAL_PROPERTY_NAME = 'approved'
APPROVAL_PROPERTY_VALUE_UNAPPROVED = False
APPROVAL_PROPERTY_VALUE_APPROVED = True

class MemberapprovalPlugin(ZODBUserManager):
    """Multi-plugin

    """
    implements(IMemberapprovalPlugin)
    meta_type = 'memberapproval Plugin'
    security = ClassSecurityInfo()

    def authenticateCredentials( self, credentials ):
        login = credentials.get( 'login' )
        password = credentials.get( 'password' )

        if login is None or password is None:
            return None

        authorized = super(MemberapprovalPlugin, self).authenticateCredentials(
                            credentials)
        if authorized is None:
            return None

        userid = self._login_to_userid.get( login, login )
        if userid:
            acl = self.acl_users
            user = acl.getUserById(userid)
            for sheet_id in user.listPropertysheets():
                sheet = user.getPropertysheet(sheet_id)
                if sheet.hasProperty(APPROVAL_PROPERTY_NAME):
                    if sheet.getProperty(APPROVAL_PROPERTY_NAME) \
                       == APPROVAL_PROPERTY_VALUE_APPROVED:
                        return authorized
                    else:
                        return None

        return None

    def approveUser(self, user_id):
        acl = self.acl_users
        user = acl.getUserById(user_id)
        for sheet_id in user.listPropertysheets():
            sheet = user.getPropertysheet(sheet_id)
            if sheet.hasProperty(APPROVAL_PROPERTY_NAME):
                sheet.setProperty(user, APPROVAL_PROPERTY_NAME, 
                                        APPROVAL_PROPERTY_VALUE_APPROVED)
                return True
        raise KeyError('No property sheet provides "' 
                           + APPROVAL_PROPERTY_NAME + '" property')

    def unapproveUser(self, user_id):
        acl = self.acl_users
        user = acl.getUserById(user_id)
        for sheet_id in user.listPropertysheets():
            sheet = user.getPropertysheet(sheet_id)
            if sheet.hasProperty(APPROVAL_PROPERTY_NAME):
                sheet.setProperty(user, APPROVAL_PROPERTY_NAME, APPROVAL_PROPERTY_VALUE_UNAPPROVED)
                return True
        raise KeyError('No property sheet provides "' + APPROVAL_PROPERTY_NAME + '" property')
        


classImplements(MemberapprovalPlugin, [IAuthenticationPlugin,
                                       IUserAdderPlugin,
                                       IUserEnumerationPlugin]),
InitializeClass( MemberapprovalPlugin )
