from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces.referenceengine import IUIDCatalog
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.uuid.interfaces import IUUID
from plone.indexer.decorator import indexer

@indexer(IReferenceable, IUIDCatalog)
def UID(obj):
    return IUUID(obj, None)

def added_handler(obj, event):
    """Index the object inside uid_catalog"""
    uid_catalog = getToolByName(obj, 'uid_catalog')
    path = '/'.join(obj.getPhysicalPath())
    uid_catalog.catalog_object(obj, path)

def modified_handler(obj, event):
    """Reindex object in uid_catalog"""
    uid_catalog = getToolByName(obj, 'uid_catalog')
    path = '/'.join(obj.getPhysicalPath())
    uid_catalog.catalog_object(obj, path)

def removed_handler(obj, event):
    """Remove object from uid_catalog"""
    uid_catalog = getToolByName(obj, 'uid_catalog')
    path = '/'.join(obj.getPhysicalPath())
    uid_catalog.uncatalog_object(path)
