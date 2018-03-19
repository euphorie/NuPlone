from five import grok
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from Products.CMFPlone.interfaces import IPloneSiteRoot

grok.templatedir("templates")


class Frontpage(grok.View):
    grok.context(IPloneSiteRoot)
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")
    grok.template("frontpage")
    grok.require("zope2.View")
