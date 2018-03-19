from five import grok
from plone.dexterity.interfaces import IDexterityContainer
from plonetheme.nuplone.skin.interfaces import NuPloneSkin

grok.templatedir("templates")


class Container(grok.View):
    grok.context(IDexterityContainer)
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")
    grok.template("frontpage")
