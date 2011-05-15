from zope.component import adapts, adapter
from zope.interface import implements, directlyProvides
from plone.uuid.interfaces import IAttributeUUID, IUUID
from Products.Archetypes.interfaces import referenceable
from Products.CMFCore.utils import getToolByName


class IReferenceable(IAttributeUUID):
    """Adds abilities to be referenced"""


class ATReferenceable(object):
    """Adapts Dexterity items using this package's referenceable behavior
    to Archetypes' IReferenceable interface.
    """
    
    adapts(IReferenceable)
    implements(referenceable.IReferenceable)
    
    def __init__(self, context):
        self.context = context
        self.tool = getToolByName(context, 'reference_catalog')
        self.uid_catalog = getToolByName(context, 'uid_catalog')
        self.portal = getToolByName(context, 'portal_url').getPortalObject()
    
    isReferenceable = 1
    
    def reference_url(self):
        # like absoluteURL, but return a link to the object with this UID"""
        return self.tool.reference_url(self)

    def hasRelationshipTo(self, target, relationship=None):
        return self.tool.hasRelationshipTo(self, target, relationship)

    def addReference(self, object, relationship=None, referenceClass=None,
                     updateReferences=True, **kwargs):
        return self.tool.addReference(self, object, relationship, referenceClass,
                                      updateReferences, **kwargs)

    def deleteReference(self, target, relationship=None):
        return self.tool.deleteReference(self, target, relationship)

    def deleteReferences(self, relationship=None):
        return self.tool.deleteReferences(self, relationship)

    def getRelationships(self):
        # What kinds of relationships does this object have
        return self.tool.getRelationships(self)

    def getBRelationships(self):
        # What kinds of relationships does this object have from others
        return self.tool.getBackRelationships(self)

    def getRefs(self, relationship=None, targetObject=None):
        # get all the referenced objects for this object
        brains = self.tool.getReferences(self, relationship, targetObject=targetObject,
                                         objects=False)
        if brains:
            return [self._optimizedGetObject(b.targetUID) for b in brains]
        return []

    def getBRefs(self, relationship=None, targetObject=None):
        # get all the back referenced objects for this object
        brains = self.tool.getBackReferences(self.context, relationship,
                                             targetObject=targetObject, objects=False)
        if brains:
            return [self._optimizedGetObject(b.sourceUID) for b in brains]
        return []

    #aliases
    getReferences=getRefs
    getBackReferences=getBRefs

    def getReferenceImpl(self, relationship=None, targetObject=None):
        # get all the reference objects for this object
        refs = self.tool.getReferences(self.context, relationship, targetObject=targetObject)
        if refs:
            return refs
        return []

    def getBackReferenceImpl(self, relationship=None, targetObject=None):
        # get all the back reference objects for this object
        refs = self.tool.getBackReferences(self.context, relationship, targetObject=targetObject)
        if refs:
            return refs
        return []

    def _optimizedGetObject(self, uid):
        tool = self.uid_catalog
        if tool is None: # pragma: no cover
            return ''
        traverse = self.portal.unrestrictedTraverse

        _catalog = tool._catalog
        rids = _catalog.indexes['UID']._index.get(uid, ())
        if isinstance(rids, int):
            rids = (rids, )

        for rid in rids:
            path = _catalog.paths[rid]
            obj = traverse(path, default=None)
            if obj is not None:
                return obj
    
    def UID(self):
        return IUUID(self.context)


@adapter(ATReferenceable)
def uuid_for_adapter(referenceable):
    return referenceable.UID()
directlyProvides(uuid_for_adapter, IUUID)
