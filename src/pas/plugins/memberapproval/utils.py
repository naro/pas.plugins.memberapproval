from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from pas.plugins.memberapproval.plugin import MemberapprovalPlugin
from pas.plugins.memberapproval.interfaces import IMemberapprovalPlugin

def getPAS():
    site=getSite()
    return getToolByName(site, "acl_users")


def getApprovalPlugin():
    pas=getPAS()
    for plugin in pas.objectValues([MemberapprovalPlugin.meta_type,]):
        if IMemberapprovalPlugin.providedBy(plugin):
            return plugin

    raise KeyError

def getSourceUsersPlugin():
    pas=getPAS()
    if 'source_users' in pas.objectIds():
        return pas['source_users']
    raise KeyError

def enablePluginInterfaces():
    # This plugin completely replaces source_users plugin!
    plugin=getApprovalPlugin()
    source_users = getSourceUsersPlugin()
    
    common_interfaces = [
            'IUserEnumerationPlugin',
            'IAuthenticationPlugin',
            'IUserAdderPlugin',
            ]


    # deactivate source_users but activate new plugin
    plugin.manage_activateInterfaces(common_interfaces)
    # Deactivate all interfaces from source_users.
    source_users.manage_activateInterfaces([])

    # Probably no need for move plugin up
    # plugins=getPAS().plugins
    # iface=plugins._getInterfaceFromName("IAuthenticationPlugin")
    # for i in range(len(plugins.listPlugins(iface))-1):
    #     plugins.movePluginsUp(iface, [plugin.getId()])
    
