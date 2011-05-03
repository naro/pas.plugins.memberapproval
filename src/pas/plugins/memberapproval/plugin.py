"""Class: MemberapprovalPlugin
"""

import copy
from BTrees.OOBTree import OOBTree
from zope.interface import implements
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.utils import classImplements
from Products.PlonePAS.plugins.user import UserManager
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserAdderPlugin
from Products.PluggableAuthService.utils import createViewName

from pas.plugins.memberapproval.interfaces import IMemberapprovalPlugin

class MemberapprovalPlugin(UserManager):
    """Multi-plugin

    """
    implements(IMemberapprovalPlugin)
    meta_type = 'memberapproval Plugin'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        super(MemberapprovalPlugin, self).__init__(id, title)
        self._activated_userid = OOBTree()

    security.declarePrivate( 'authenticateCredentials' )
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
            if self._activated_userid.get(userid):
                return authorized
            else:
                return None

        return None

    security.declarePrivate( 'userApproved' )
    def userApproved(self, user_id):
        return self._activated_userid.get(user_id, False)

    security.declarePrivate( 'approveUser' )
    def approveUser(self, user_id):
        self._activated_userid[user_id] = True

    security.declarePrivate( 'unapproveUser' )
    def unapproveUser(self, user_id):
        self._activated_userid[user_id] = False

    security.declarePrivate( 'addUser' )
    def addUser( self, user_id, login_name, password ):
        self._activated_userid[ user_id ] = False
        return super(MemberapprovalPlugin, self).addUser(user_id, login_name, password)

    #
    #   IUserEnumerationPlugin implementation
    #
    # If I want to use custom _ZODBUserFilter I have to use
    # custom enumerateUsers method. See description before _ZODBUserFilter
    # implementation below.
    security.declarePrivate( 'enumerateUsers' )
    def enumerateUsers( self
                      , id=None
                      , login=None
                      , exact_match=False
                      , sort_by=None
                      , max_results=None
                      , **kw
                      ):
    
        """ See IUserEnumerationPlugin.
        """
        user_info = []
        user_ids = []
        plugin_id = self.getId()
        view_name = createViewName('enumerateUsers', id or login)
    
    
        if isinstance( id, basestring ):
            id = [ id ]
    
        if isinstance( login, basestring ):
            login = [ login ]
    
        # Look in the cache first...
        keywords = copy.deepcopy(kw)
        keywords.update( { 'id' : id
                         , 'login' : login
                         , 'exact_match' : exact_match
                         , 'sort_by' : sort_by
                         , 'max_results' : max_results
                         }
                       )
        cached_info = self.ZCacheable_get( view_name=view_name
                                         , keywords=keywords
                                         , default=None
                                         )
        if cached_info is not None:
            return tuple(cached_info)
    
        terms = id or login
    
        if exact_match:
            if terms:
    
                if id:
                    # if we're doing an exact match based on id, it
                    # absolutely will have been qualified (if we have a
                    # prefix), so we can ignore any that don't begin with
                    # our prefix
                    id = [ x for x in id if x.startswith(self.prefix) ]
                    user_ids.extend( [ x[len(self.prefix):] for x in id ] )
                elif login:
                    user_ids.extend( [ self._login_to_userid.get( x )
                                       for x in login ] )
    
                # we're claiming an exact match search, if we still don't
                # have anything, better bail.
                if not user_ids:
                    return ()
            else:
                # insane - exact match with neither login nor id
                return ()
    
        if user_ids:
            user_filter = None
    
        else:   # Searching
            user_ids = self.listUserIds()
            user_filter = _ZODBUserFilter( id, login, **kw )
    
        for user_id in user_ids:
    
            if self._userid_to_login.get( user_id ):
                e_url = '%s/manage_users' % self.getId()
                qs = 'user_id=%s' % user_id
    
                info = { 'id' : self.prefix + user_id
                       , 'login' : self._userid_to_login[ user_id ]
                       , 'pluginid' : plugin_id
                       , 'editurl' : '%s?%s' % (e_url, qs)
                       , 'approved' : self._activated_userid.get( user_id, False)
                       } 
    
                if not user_filter or user_filter( info ):
                    user_info.append( info )
    
        # Put the computed value into the cache
        self.ZCacheable_set(user_info, view_name=view_name, keywords=keywords)
    
        return tuple( user_info )

classImplements(MemberapprovalPlugin, [IAuthenticationPlugin,
                                       IUserAdderPlugin,
                                       IUserEnumerationPlugin]),
InitializeClass( MemberapprovalPlugin )

# I had to override this class, because it does not take **kw 
# into account. The original class contains:
#       elif self._filter_keywords:
#           return 0    # TODO:  try using 'kw'
# so I replaced return 0 with proper search by keyword (property)
# 
# Additionally, if I want to use custom _ZODBUserFilter I have to use
# custom enumerateUsers method above
class _ZODBUserFilter:

    def __init__( self
                , id=None
                , login=None
                , **kw
                ):

        self._filter_ids = id
        self._filter_logins = login
        self._filter_keywords = kw

    def __call__( self, user_info ):

        if self._filter_ids:

            key = 'id'
            to_test = self._filter_ids

        elif self._filter_logins:

            key = 'login'
            to_test = self._filter_logins

        elif self._filter_keywords:
            for k, v in self._filter_keywords.items():
                if k in user_info.keys():
                    return v == user_info[k]
            return 0
        else:
            return 1    # the search is done without any criteria

        value = user_info.get( key )

        if not value:
            return 0

        for contained in to_test:
            if value.lower().find( contained.lower() ) >= 0:
                return 1

        return 0