from pas.plugins.memberapproval import install
install.register_memberapproval_plugin()

from pas.plugins.memberapproval import paspatch

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    install.register_memberapproval_plugin_class(context)
    import pdb; pdb.set_trace( )
    # PluginInfo = {
    #     'id' : 'IMemberApprovalPlugin',
    #     'title': 'member_approval',
    #     'description': "Provided member approval functions"
    #     }
    # pas = context.acl_users
    # registerPluginType(pas, IMemberApprovalPlugin, PluginInfo)
