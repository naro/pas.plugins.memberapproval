from AccessControl.Permissions import manage_users
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin

import plugin

manage_add_memberapproval_form = PageTemplateFile('browser/add_plugin',
                            globals(), __name__='manage_add_memberapproval_form' )


def manage_add_memberapproval_plugin( dispatcher, id, title=None, REQUEST=None ):
    """Add an memberapproval Plugin to the PluggableAuthentication Service."""

    sp = plugin.MemberapprovalPlugin( id, title )
    dispatcher._setObject( sp.getId(), sp )

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect( '%s/manage_workspace'
                                      '?manage_tabs_message='
                                      'memberapprovalPlugin+added.'
                                      % dispatcher.absolute_url() )


def register_memberapproval_plugin():
    try:
        registerMultiPlugin(plugin.MemberapprovalPlugin.meta_type)
    except RuntimeError:
        # make refresh users happy
        pass


def register_memberapproval_plugin_class(context):
    context.registerClass(plugin.MemberapprovalPlugin,
                          permission = manage_users,
                          constructors = (manage_add_memberapproval_form,
                                          manage_add_memberapproval_plugin),
                          visibility = None,
                          icon='browser/icon.gif'
                         )
