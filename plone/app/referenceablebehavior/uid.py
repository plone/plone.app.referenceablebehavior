from plone.uuid.interfaces import IAttributeUUID, IUUID
from plone.indexer.decorator import indexer

#should be moved to Products.CMFPlone
@indexer(IAttributeUUID)
def indexer(obj):
    return IUUID(obj, None)
