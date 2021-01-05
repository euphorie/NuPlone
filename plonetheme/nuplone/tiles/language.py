from plone.tiles import Tile
from plonetheme.nuplone.utils import viewType
from Products.CMFCore.utils import getToolByName


class LanguageTile(Tile):
    def update(self):
        lt = getToolByName(self.context, "portal_languages")
        languages = [
            _ for _ in lt.getAvailableLanguageInformation().values() if _["selected"]
        ]
        languages.sort(key=lambda l: l.get("native", l["name"]))
        self.languages = languages
        self.current_language = lt.getPreferredLanguage()

    def __call__(self):
        view_type = viewType(self.context, self.request)
        if view_type in ["add", "edit"]:
            return None

        self.update()
        return self.index()
