from plone.tiles import Tile
from Products.CMFCore.utils import getToolByName

class LanguageTile(Tile):
    def update(self):
        lt=getToolByName(self.context, "portal_languages")
        languages=[l for l in lt.getAvailableLanguageInformation().values()
                   if l["selected"]]
        languages.sort(key=lambda l: l.get("native", l["name"]))
        self.languages=languages
        self.current_language=lt.getPreferredLanguage()


    def __call__(self):
        self.update()
        return self.index()
