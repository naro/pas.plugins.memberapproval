from Products.PlonePAS.Extensions.Install import registerPluginType
from pas.plugins.memberapproval.interfaces import IMemberApprovalPlugin

def setupVarious(context):
    if context.readDataFile('pas.plugins.memberapproval.txt') is None:
        return 

    site = context.getSite()

    PluginInfo = {
        'id' : 'IMemberApprovalPlugin',
        'title': 'member_approval',
        'description': "Provided member approval functions"
        }
    pas = site.acl_users
    registerPluginType(pas, IMemberApprovalPlugin, PluginInfo)
    
    