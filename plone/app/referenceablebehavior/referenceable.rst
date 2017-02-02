Referenceable behavior
======================

Archetypes base classes are Referenceable. To be able to link
dexterity content types from archetypes content types you need
to activate that behavior

So first lets create a new dexterity content type

    >>> from plone.dexterity.fti import DexterityFTI
    >>> fti = DexterityFTI('referenceable_type')
    >>> fti.behaviors = ('plone.app.dexterity.behaviors.metadata.IDublinCore',
    ...                  'plone.app.referenceablebehavior.referenceable.IReferenceable')
    >>> portal = layer['portal']
    >>> app = layer['app']
    >>> portal.portal_types._setObject('referenceable_type', fti)
    'referenceable_type'
    >>> schema = fti.lookupSchema()
    >>> from transaction import commit
    >>> commit()

If we access the site as an admin TTW::

    >>> from plone.testing.z2 import Browser
    >>> browser = Browser(app)
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))

We can see this type in the addable types at the root of the site::

    >>> browser.open("http://nohost/plone/folder_factories")
    >>> "referenceable_type" in browser.contents
    True
    >>> browser.getControl("referenceable_type").click()
    >>> browser.getControl("Add").click()
    >>> browser.getControl(name="form.widgets.IDublinCore.title").value = "My Object"
    >>> browser.getControl(name="form.widgets.IDublinCore.description").value = "Lorem ipsum"
    >>> browser.getControl(name="form.buttons.save").click()
    >>> browser.url
    'http://nohost/plone/referenceable_type/view'

Now lets check that we have uuid stuff

    >>> item = portal.referenceable_type
    >>> from plone.app.referenceablebehavior.referenceable import IReferenceable
    >>> IReferenceable.providedBy(item)
    True
    >>> from plone.uuid.interfaces import IAttributeUUID
    >>> IAttributeUUID.providedBy(item)
    True
    >>> from plone.uuid.interfaces import ATTRIBUTE_NAME
    >>> uuid = getattr(item, ATTRIBUTE_NAME, None)
    >>> uuid is not None
    True

Now create an archetype content object.

    >>> from plone.app.testing import setRoles
    >>> from plone.app.testing import TEST_USER_ID
    >>> setRoles(portal, TEST_USER_ID, ['Manager'])
    >>> _ = portal.invokeFactory('ATRefnode', "archetype-page",
    ...                          title="archetype page")
    >>> commit()

Now add the dexterity content as reference in archetype page

It seems there is no way to use related items with functional tests
###    >>> browser.getLink('Edit').click()

    >>> archetypes = getattr(portal,'archetype-page')
    >>> dexterity = getattr(portal,'referenceable_type')
    >>> from plone.uuid.interfaces import IUUID
    >>> uuid = IUUID(dexterity)
    >>> archetypes.setRelatedItems([uuid])
    >>> archetypes.reindexObject()
    >>> archetypes.getRelatedItems()
    [<Item at /plone/referenceable_type>]
    >>> commit()

A dexterity could be adapted to Archetypes IReferenceable

    >>> from Products.Archetypes.interfaces import referenceable
    >>> referenceable_dexterity = referenceable.IReferenceable(dexterity)
    >>> referenceable_dexterity.isReferenceable
    1
    >>> referenceable_dexterity.reference_url()
    'http://nohost/plone/reference_catalog/lookupObject?uuid=...'
    >>> referenceable_dexterity.UID() == uuid
    True
    >>> IUUID(referenceable_dexterity) == uuid
    True
    >>> referenceable_dexterity.getId()
    'referenceable_type'

Now create another dexterity referenceable object

    >>> browser.open("http://nohost/plone/folder_factories")
    >>> browser.getControl("referenceable_type").click()
    >>> browser.getControl("Add").click()
    >>> browser.getControl(name="form.widgets.IDublinCore.title").value = "Another Object"
    >>> browser.getControl(name="form.widgets.IDublinCore.description").value = "Lorem ipsum"
    >>> browser.getControl(name="form.buttons.save").click()
    >>> browser.url
    'http://nohost/plone/referenceable_type-1/view'
    >>> dexterity1 = getattr(portal,'referenceable_type-1')
    >>> referenceable_dexterity1 = referenceable.IReferenceable(dexterity1)

    >>> def catalog_get_all(catalog, unique_idx='UID'):
    ...     """Get all brains from the catalog.
    ...     """
    ...     res = [
    ...         catalog({
    ...             unique_idx: catalog._catalog.getIndexDataForRID(it)[unique_idx]
    ...         })[0]
    ...         for it in catalog._catalog.data
    ...     ]
    ...     return res


    >>> reference_catalog = portal.reference_catalog

    >>> 'relatesTo' in [b.relationship for b in catalog_get_all(reference_catalog)]
    True
    >>> 'isReferencing' in [b.relationship for b in catalog_get_all(reference_catalog)]
    False

We can add references between archetypes and dexterity content

    >>> archetypes.addReference(referenceable_dexterity1,
    ...                         'isReferencing')
    <Reference... rel:isReferencing>
    >>> 'relatesTo' in [b.relationship for b in catalog_get_all(reference_catalog)]
    True
    >>> 'isReferencing' in [b.relationship for b in catalog_get_all(reference_catalog)]
    True

We can get back references from dexterity content

    >>> referenceable_dexterity1.getBRelationships()
    ['isReferencing']
    >>> referenceable_dexterity1.getBRefs()
    [<ATRefnode at /plone/archetype-page>]

We can add references between archetypes and dexterity content

    >>> referenceable_dexterity1.hasRelationshipTo(archetypes)
    False
    >>> referenceable_dexterity1.getRelationships()
    []
    >>> referenceable_dexterity1.getRefs()
    []
    >>> referenceable_dexterity1.addReference(archetypes,
    ...                         'isReferencing')
    <Reference... rel:isReferencing>
    >>> referenceable_dexterity1.hasRelationshipTo(archetypes)
    True
    >>> referenceable_dexterity1.getRelationships()
    ['isReferencing']
    >>> referenceable_dexterity1.getRefs()
    [<ATRefnode at /plone/archetype-page>]
    >>> referenceable_dexterity1.getReferenceImpl()
    [<Reference ... rel:isReferencing>]
    >>> referenceable_dexterity1.getBackReferenceImpl()
    [<Reference ... rel:isReferencing>]

We can get back references from archetypes to dexterity content

    >>> archetypes.getBRelationships()
    ['isReferencing']
    >>> archetypes.getBRefs()
    [<Item at /plone/referenceable_type-1>]

We can add references between dexterity objects

    >>> referenceable_dexterity1.hasRelationshipTo(referenceable_dexterity)
    False
    >>> referenceable_dexterity1.addReference(referenceable_dexterity,
    ...                         'isReferencing')
    <Reference... rel:isReferencing>
    >>> referenceable_dexterity1.hasRelationshipTo(referenceable_dexterity)
    True
    >>> referenceable_dexterity1.getRelationships()
    ['isReferencing']
    >>> refs = [i.getId() for i in referenceable_dexterity1.getRefs()]
    >>> 'archetype-page' in refs
    True
    >>> 'referenceable_type' in refs
    True
    >>> len(refs)
    2

We can remove references

    >>> referenceable_dexterity1.deleteReference(referenceable_dexterity)
    >>> referenceable_dexterity1.hasRelationshipTo(referenceable_dexterity)
    False
    >>> referenceable_dexterity1.getRelationships()
    ['isReferencing']
    >>> referenceable_dexterity1.getRefs()
    [<ATRefnode at /plone/archetype-page>]
    >>> referenceable_dexterity1.deleteReferences()
    >>> referenceable_dexterity1.getRelationships()
    []
    >>> referenceable_dexterity1.getRefs()
    []
