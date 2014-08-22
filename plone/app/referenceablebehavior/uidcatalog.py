from Products.Archetypes import config
from Products.Archetypes.interfaces import IReferenceable as IATReferenceable
from Products.Archetypes.interfaces.referenceengine import IUIDCatalog
from Products.Archetypes.utils import getRelURL
from Products.CMFCore.utils import getToolByName
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.indexer.decorator import indexer
from plone.uuid.interfaces import IUUID
from zope.component.hooks import getSite


@indexer(IReferenceable, IUIDCatalog)
def UID(obj):
    return IUUID(obj, None)


def _get_catalogs(obj):
    try:
        uid_catalog = getToolByName(obj, config.UID_CATALOG)
    except AttributeError:
        uid_catalog = getToolByName(getSite(), config.UID_CATALOG)
    try:
        ref_catalog = getToolByName(obj, config.REFERENCE_CATALOG)
    except AttributeError:
        ref_catalog = getToolByName(getSite(), config.REFERENCE_CATALOG)
    return uid_catalog, ref_catalog


def added_handler(obj, event):
    """Index the object inside uid_catalog"""
    uid_catalog, ref_catalog = _get_catalogs(obj)
    path = '/'.join(obj.getPhysicalPath())
    uid_catalog.catalog_object(obj, path)


def modified_handler(obj, event):
    """Reindex object in uid_catalog"""
    uid_catalog, ref_catalog = _get_catalogs(obj)
    path = '/'.join(obj.getPhysicalPath())
    uid_catalog.catalog_object(obj, path)

    #  AT API
    annotations = IATReferenceable(obj)._getReferenceAnnotations()
    if not annotations:
        return

    for ref in annotations.objectValues():
        url = getRelURL(ref_catalog, ref.getPhysicalPath())
        uid_catalog.catalog_object(ref, url)
        ref_catalog.catalog_object(ref, url)
        ref._catalogRefs(uid_catalog, uid_catalog, ref_catalog)


def moved_handler(obj, event):
    """Remove object from uid_catalog and add it back"""
    # Not sure if this is the proper way to handle it.
    # it is needed because of what happens in Products.ZCatalog.Catalog.py
    # line 317.
    # When path has changed, the object cannot be found, and we end up with
    # old and invalid uids.
    uid_catalog, ref_catalog = _get_catalogs(obj)
    uid = IUUID(obj.aq_base, None)

    if uid:
        results = uid_catalog(UID=uid)

        if len(results) > 0:
            old_obj = results[0]
            uid_catalog.uncatalog_object(old_obj.getPath())
            path = '/'.join(obj.getPhysicalPath())
            uid_catalog.catalog_object(obj, path)

    #  AT API
    annotations = IATReferenceable(obj)._getReferenceAnnotations()
    if not annotations:
        return

    for ref in annotations.objectValues():
        url = getRelURL(ref_catalog, ref.getPhysicalPath())
        if event.oldName and event.newName:
            url = event.oldName + url[len(event.newName):]
        uid_catalog_rid = uid_catalog.getrid(url)
        ref_catalog_rid = ref_catalog.getrid(url)
        if uid_catalog_rid is not None:
            uid_catalog.uncatalog_object(url)
        if ref_catalog_rid is not None:
            ref_catalog.uncatalog_object(url)


def removed_handler(obj, event):
    """Remove object from uid_catalog"""
    uid_catalog, ref_catalog = _get_catalogs(obj)
    path = '/'.join(obj.getPhysicalPath())
    uid_catalog.uncatalog_object(path)
