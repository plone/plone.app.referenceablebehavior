from Products.CMFCore.utils import getToolByName

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
    #TODO: ObjectRemoed event is triggered to much
#    try:
#        uid_catalog.uncatalog_object(obj)
#    except:
#        pass
