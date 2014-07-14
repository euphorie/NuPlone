from plonetheme.nuplone.auth import LoginChallenger
import logging

log = logging.getLogger(__name__)

def setupVarious(context):
    if context.readDataFile('plonetheme.nuplone.txt') is None:
        return
    addNuploneChallengerPlugin(context)

def addNuploneChallengerPlugin(context):
    site = context.getSite()
    pas = site.acl_users
    if not pas.objectIds([LoginChallenger.meta_type]):
        plugin = LoginChallenger("nuplone-challenger", LoginChallenger.meta_type)
        pas._setObject(plugin.getId(), plugin)
        plugin = getattr(pas, plugin.getId())

        infos = [info for info in pas.plugins.listPluginTypeInfo()
               if plugin.testImplements(info["interface"])]
        plugin.manage_activateInterfaces([info["id"] for info in infos])
        for info in infos:
            for i in range(len(pas.plugins.listPluginIds(info["interface"]))):
                pas.plugins.movePluginsUp(info["interface"], [plugin.getId()])
