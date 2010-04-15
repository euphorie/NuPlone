from zope.interface import Interface
from five import grok
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone import utils

grok.templatedir("templates")

class Sitemenu(grok.View):
    grok.context(Interface)
    grok.name("sitemenu")
    grok.layer(NuPloneSkin)
    grok.template("sitemenu")

