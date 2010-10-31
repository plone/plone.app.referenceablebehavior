from plone.uuid.interfaces import IAttributeUUID, IUUID
from plone.indexer.decorator import indexer
from Products.Archetypes.interfaces.referenceengine import IUIDCatalog

class IReferenceable(IAttributeUUID):
    """Adds abilities to be referenced"""

@indexer(IReferenceable)
def catalogtool_indexer(obj):
    return IUUID(obj, None)

@indexer(IReferenceable, IUIDCatalog)
def uidcatalog_indexer(obj):
    return IUUID(obj, None)
