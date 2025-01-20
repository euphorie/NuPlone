from plone import api
from zope.schema.vocabulary import getVocabularyRegistry
from zope.schema.vocabulary import VocabularyRegistryError


def getVocabulary(field):
    if field.vocabulary is not None:
        return field.vocabulary

    vr = getVocabularyRegistry()
    try:
        return vr.get(None, field.vocabularyName)
    except AttributeError:
        # Most probably it is safe to always pass the portal to vr.get.
        # Anyway this patch minimizes the risk of breaking something.
        try:
            return vr.get(api.portal.get(), field.vocabularyName)
        except VocabularyRegistryError:
            return None
    except VocabularyRegistryError:
        return None
