from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces.referenceengine import IUIDCatalog
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.uuid.interfaces import IUUID
from plone.indexer.decorator import indexer
from zope.component.hooks import getSite


@indexer(IReferenceable, IUIDCatalog)
def UID(obj):
    return IUUID(obj, None)


def _get_catalog(obj):
    try:
        return getToolByName(obj, 'uid_catalog')
    except AttributeError:
        return getToolByName(getSite(), 'uid_catalog')


def added_handler(obj, event):
    """Index the object inside uid_catalog"""
    uid_catalog = _get_catalog(obj)
    path = '/'.join(obj.getPhysicalPath())
    uid_catalog.catalog_object(obj, path)


def modified_handler(obj, event):
    """Reindex object in uid_catalog"""
    uid_catalog = _get_catalog(obj)
    path = '/'.join(obj.getPhysicalPath())
    uid_catalog.catalog_object(obj, path)


def moved_handler(obj, event):
    """Remove object from uid_catalog and add it back"""
    # Not sure if this is the proper way to handle it.
    # it is needed because of what happens in Products.ZCatalog.Catalog.py
    # line 317.
    # When path has changed, the object cannot be found, and we end up with
    # old and invalid uids.
    uid_catalog = _get_catalog(obj)
    uid = IUUID(obj.aq_base, None)

    if uid:
        results = uid_catalog(UID=uid)

        if len(results) > 0:
            old_obj = results[0]
            uid_catalog.uncatalog_object(old_obj.getPath())
            path = '/'.join(obj.getPhysicalPath())
            uid_catalog.catalog_object(obj, path)


def removed_handler(obj, event):
    """Remove object from uid_catalog"""
    uid_catalog = _get_catalog(obj)
    path = '/'.join(obj.getPhysicalPath())
    uid_catalog.uncatalog_object(path)
