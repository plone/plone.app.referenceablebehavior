from plone.uuid.interfaces import IAttributeUUID, IUUID
from plone.indexer.decorator import indexer
from Products.Archetypes.interfaces.referenceengine import IUIDCatalog

class IReferenceable(IAttributeUUID):
    """Adds abilities to be referenced"""
