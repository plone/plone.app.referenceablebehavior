from plone.uuid.interfaces import IAttributeUUID, IUUID
from plone.indexer.decorator import indexer

class IReferenceable(IAttributeUUID):
    """Adds abilities to be referenced"""

@indexer(IReferenceable)
def uuidIndexer(obj):
    return IUUID(obj, None)
