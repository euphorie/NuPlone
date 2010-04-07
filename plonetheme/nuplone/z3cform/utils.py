from zope.schema.vocabulary import getVocabularyRegistry
from zope.schema.vocabulary import VocabularyRegistryError

def getVocabulary(field):
    if field.vocabulary is not None:
        return field.vocabulary

    vr=getVocabularyRegistry()
    try:
        return vr.get(None, field.vocabularyName)
    except VocabularyRegistryError:
        return None



