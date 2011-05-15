from plone.app.referenceablebehavior.tests.base import ReferenceableFunctionalTestCase


class TestATReferenceable(ReferenceableFunctionalTestCase):
    
    def _makeOne(self):
        # create a referenceable type
        from plone.dexterity.fti import DexterityFTI
        fti = DexterityFTI('referenceable_type')
        fti.behaviors = ('plone.app.referenceablebehavior.referenceable.IReferenceable',)
        self.portal.portal_types._setObject('referenceable_type', fti)

        # add one to the site
        self.setRoles(['Manager'])
        self.item = self.portal[self.portal.invokeFactory('referenceable_type', 'item')]
        
        # add a normal page with a reference to it
        self.page = self.portal[self.portal.invokeFactory('Document', 'page')]
        self.page.setRelatedItems([self.item])
        
        # return its AT adapter
        from Products.Archetypes.interfaces.referenceable import IReferenceable
        return IReferenceable(self.item)
    
    def test_provides_interface(self):
        ref = self._makeOne()

        from Products.Archetypes.interfaces.referenceable import IReferenceable
        self.assertTrue(IReferenceable.providedBy(ref))

    def test_reference_url(self):
        ref = self._makeOne()
        self.assertEqual(
            'http://nohost/plone/reference_catalog/lookupObject?uuid=' + ref.UID(),
            ref.reference_url())

    def test_hasRelationshipTo(self):
        ref = self._makeOne()
        ref.addReference(self.page, 'being_tested_with')
        self.assertTrue(ref.hasRelationshipTo(self.page))
