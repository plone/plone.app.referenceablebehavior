# -*- coding: utf-8 -*-
from Acquisition import aq_base
from zope.component import adapts, adapter
from zope.interface import implementer, directlyProvides
from plone.uuid.interfaces import IAttributeUUID, IUUID
from Products.Archetypes import config
from Products.Archetypes.interfaces import referenceable
from Products.Archetypes.ReferenceEngine import Reference as BaseReference
from Products.Archetypes.utils import getRelURL
from Products.CMFCore.utils import getToolByName
from OFS.Folder import Folder


class IReferenceable(IAttributeUUID):
    """Adds abilities to be referenced"""


class Reference(BaseReference):

    def getSourceObject(self):
        obj = self._optimizedGetObject(self.sourceUID)
        if obj and not referenceable.IReferenceable.providedBy(obj):
            obj = referenceable.IReferenceable(obj)
        return obj

    def getTargetObject(self):
        obj = self._optimizedGetObject(self.targetUID)
        if obj and not referenceable.IReferenceable.providedBy(obj):
            obj = referenceable.IReferenceable(obj)
        return obj

    def manage_afterAdd(self, item, container):
        ct = getToolByName(container, config.REFERENCE_CATALOG, None)
        self._register(reference_manager=ct)
        self._updateCatalog(container)
        self._referenceApply('manage_afterAdd', item, container)
        base = container
        rc = getToolByName(container, config.REFERENCE_CATALOG)
        url = getRelURL(base, self.getPhysicalPath())
        rc.catalog_object(self, url)


@implementer(referenceable.IReferenceable)
class ATReferenceable(object):
    """Adapts Dexterity items using this package's referenceable behavior
    to Archetypes' IReferenceable interface.
    """

    adapts(IReferenceable)

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

    def addReference(self, object, relationship=None, referenceClass=Reference,
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
        brains = self.tool.getBackReferences(self, relationship,
                                             targetObject=targetObject, objects=False)
        if brains:
            return [self._optimizedGetObject(b.sourceUID) for b in brains]
        return []

    #aliases
    getReferences=getRefs
    getBackReferences=getBRefs

    def getReferenceImpl(self, relationship=None, targetObject=None):
        # get all the reference objects for this object
        refs = self.tool.getReferences(self, relationship, targetObject=targetObject)
        if refs:
            return refs
        return []

    def getBackReferenceImpl(self, relationship=None, targetObject=None):
        # get all the back reference objects for this object
        refs = self.tool.getBackReferences(self, relationship, targetObject=targetObject)
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

    def _getReferenceAnnotations(self):
        # given an object, extract the bag of references for which it is the
        # source
        if not getattr(aq_base(self.context), config.REFERENCE_ANNOTATION, None):
            setattr(self.context, config.REFERENCE_ANNOTATION,
                    Folder(config.REFERENCE_ANNOTATION))

        return getattr(self.context, config.REFERENCE_ANNOTATION).__of__(self.context)

    def UID(self):
        return IUUID(self.context)

    def getId(self):
        return self.context.getId()


@adapter(ATReferenceable)
def uuid_for_adapter(referenceable):
    return referenceable.UID()
directlyProvides(uuid_for_adapter, IUUID)
