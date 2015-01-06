Indexation in UIDCatalog
========================

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
    >>> browser.handleErrors = False
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

First check it is indexed in the uid_catalog

    >>> from plone.uuid.interfaces import IUUID
    >>> uuid = IUUID(portal.referenceable_type)
    >>> uid_catalog = portal.uid_catalog
    >>> results = uid_catalog(UID=uuid)
    >>> len(results)
    1
    >>> results[0].Title
    'My Object'

Now let's see that if we modified the object, the catalog is updated

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name="form.widgets.IDublinCore.title").value = "My Modified Object"
    >>> browser.getControl(name="form.buttons.save").click()
    >>> 'Changes saved' in browser.contents
    True

    >>> results = uid_catalog(UID=uuid)
    >>> results[0].Title
    'My Modified Object'

If we move the object, the catalog gets updated

    >>> results[0].getPath()
    '/plone/referenceable_type'

    >>> browser.getLink("Cut").click()

    >>> browser.open("http://nohost/plone")
    >>> browser.getLink("Add new").click()
    >>> browser.getControl("Folder").selected = True
    >>> browser.getControl("Add").click()
    >>> browser.getControl("Title").value = "My Folder"
    >>> browser.getControl("Save").click()
    >>> browser.getLink("Paste").click()

    >>> results = uid_catalog(UID=uuid)
    >>> results[0].getPath()
    '/plone/my-folder/referenceable_type'

If we try to delete, there is a confirmation screen. If we cancel, the item is
not deleted and the item remains catalogued.

    >>> browser.open("http://nohost/plone/my-folder")
    >>> browser.getLink("My Modified Object").click()
    >>> browser.getLink(url='http://nohost/plone/my-folder/referenceable_type/delete_confirmation').click()
    >>> browser.getControl('Cancel').click()
    >>> results = uid_catalog(UID=uuid)
    >>> len(results)
    1

However, if we confirm the deletion, the item is removed and the UID is no
longer catalogued.

    >>> browser.getLink(url='http://nohost/plone/my-folder/referenceable_type/delete_confirmation').click()
    >>> browser.getControl('Delete').click()
    >>> results = uid_catalog(UID=uuid)
    >>> len(results)
    0
