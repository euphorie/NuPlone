def initialize(context):
    from AccessControl.Permissions import manage_users as ManageUsers
    from Products.PluggableAuthService.PluggableAuthService import registerMultiPlugin
    from euphorie.client import authentication

    registerMultiPlugin(authentication.EuphorieAccountPlugin.meta_type)
    context.registerClass(authentication.EuphorieAccountPlugin,
                          permission=ManageUsers,
                                constructors=
                                        (authentication.manage_addEuphorieAccountPlugin,
                                        authentication.addEuphorieAccountPlugin),
                                visibility=None)

