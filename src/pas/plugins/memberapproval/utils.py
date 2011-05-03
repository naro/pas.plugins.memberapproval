from copy import deepcopy
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from pas.plugins.memberapproval.plugin import MemberapprovalPlugin
from pas.plugins.memberapproval.interfaces import IMemberApprovalPlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

def getPAS():
    site=getSite()
    return getToolByName(site, "acl_users")


def getApprovalPlugin():
    pas=getPAS()
    for plugin in pas.objectValues([MemberapprovalPlugin.meta_type,]):
        if IMemberApprovalPlugin.providedBy(plugin):
            return plugin

    raise KeyError('Could not find installed member approval PAS plugin')

def getSourceUsersPlugin():
    pas=getPAS()
    if 'source_users' in pas.objectIds():
        return pas['source_users']
    return None

def enablePluginInterfaces():
    # This plugin completely replaces source_users plugin!
    plugin=getApprovalPlugin()

    source_users = getSourceUsersPlugin()
    
    common_interfaces = [
            'IUserEnumerationPlugin',
            'IAuthenticationPlugin',
            'IUserAdderPlugin',
            'IUserManagement', 
            'IUserIntrospection',
            ]


    # deactivate source_users but activate new plugin
    plugin.manage_activateInterfaces(common_interfaces)
    if source_users is not None:
        su_was_active = source_users.getId() in \
                            getPAS()['plugins'].listPluginIds(IAuthenticationPlugin)
        # Deactivate all interfaces from source_users.
        source_users.manage_activateInterfaces([])
        # if source users was active plugin for authentication, 
        # migrate all data from it to approval plugin
        if su_was_active:
            plugin._user_passwords = deepcopy(source_users._user_passwords)
            plugin._login_to_userid = deepcopy(source_users._login_to_userid)
            plugin._userid_to_login = deepcopy(source_users._userid_to_login)

    # Probably no need for move plugin up
    # plugins=getPAS().plugins
    # iface=plugins._getInterfaceFromName("IAuthenticationPlugin")
    # for i in range(len(plugins.listPlugins(iface))-1):
    #     plugins.movePluginsUp(iface, [plugin.getId()])
    
