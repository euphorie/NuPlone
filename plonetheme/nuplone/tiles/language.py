from plone.tiles import Tile
from Products.CMFCore.utils import getToolByName
from plonetheme.nuplone.utils import viewType

class LanguageTile(Tile):
    def update(self):
        lt=getToolByName(self.context, "portal_languages")
        languages=[l for l in lt.getAvailableLanguageInformation().values()
                   if l["selected"]]
        languages.sort(key=lambda l: l.get("native", l["name"]))
        self.languages=languages
        self.current_language=lt.getPreferredLanguage()

    def __call__(self):
        view_type=viewType(self.context, self.request)
        if view_type in ["add", "edit"]:
            return None

        self.update()
        return self.index()
