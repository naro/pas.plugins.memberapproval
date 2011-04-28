Tests for pas.plugins.memberapproval

test setup
----------

    >>> from Testing.ZopeTestCase import user_password
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()

Plugin setup
------------

    >>> acl_users_url = "%s/acl_users" % self.portal.absolute_url()
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % ('portal_owner', user_password))
    >>> browser.open("%s/manage_main" % acl_users_url)
    >>> browser.url
    'http://nohost/plone/acl_users/manage_main'
    >>> form = browser.getForm(index=0)
    >>> select = form.getControl(name=':action')

pas.plugins.memberapproval should be in the list of installable plugins:

    >>> 'Memberapproval Plugin' in select.displayOptions
    True

and we can select it:

    >>> select.getControl('Memberapproval Plugin').click()
    >>> select.displayValue
    ['Memberapproval Plugin']
    >>> select.value
    ['manage_addProduct/pas.plugins.memberapproval/manage_add_memberapproval_plugin_form']

we add 'Memberapproval Plugin' to acl_users:

    >>> from pas.plugins.memberapproval.plugin import MemberapprovalPlugin
    >>> myplugin = MemberapprovalPlugin('myplugin', 'Memberapproval Plugin')
    >>> self.portal.acl_users['myplugin'] = myplugin

and so on. Continue your tests here

    >>> 'ALL OK'
    'ALL OK'

