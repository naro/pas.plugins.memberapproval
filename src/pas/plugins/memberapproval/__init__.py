from pas.plugins.memberapproval import install

install.register_memberapproval_plugin()

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    install.register_memberapproval_plugin_class(context)
