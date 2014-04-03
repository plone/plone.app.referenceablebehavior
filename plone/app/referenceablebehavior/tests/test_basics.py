import unittest

from Products.Archetypes.interfaces import referenceable
from plone.uuid.interfaces import IUUID

from plone.app.referenceablebehavior.testing import PLONE_APP_REFERENCEABLE_FUNCTION_TESTING

class ReferenceableTests(unittest.TestCase):
    
    layer = PLONE_APP_REFERENCEABLE_FUNCTION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_has_uuid(self):
        doc = self.portal['doc1']
        self.assertEquals(32, len(IUUID(doc)))

    def test_rename_does_not_change_uuid(self):
        doc = self.portal['doc1']
        old_doc_uuid = IUUID(doc)
        self.portal.manage_renameObject(id='doc1', new_id='new_name')
        self.assertEquals(old_doc_uuid, IUUID(self.portal['new_name']))

    def test_referenceable_api(self):
        doc1 = self.portal['doc1']
        doc2 = self.portal['doc2']
        doc3 = self.portal['doc3']
        adapter1 = referenceable.IReferenceable(doc1)
        adapter2 = referenceable.IReferenceable(doc2)
        adapter3 = referenceable.IReferenceable(doc3)
        
        adapter1.addReference(adapter2, relationship='alpha')
        adapter3.addReference(adapter1, relationship='beta')
       
        self.assertEquals([doc2], adapter1.getRefs())
        self.assertEquals([doc3], adapter1.getBRefs())

        # Just an alias
        self.assertEquals(adapter1.getRefs(), adapter1.getReferences())
        self.assertEquals(adapter1.getBRefs(), adapter1.getBackReferences())

        # ReferenceObjects
        references = adapter1.getReferenceImpl()
        self.assertEquals(1, len(references))
        self.assertEquals(doc1, references[0].getSourceObject().context)
        self.assertEquals(doc2, references[0].getTargetObject().context)
        self.assertEquals('alpha', references[0].relationship)

        references = adapter1.getBackReferenceImpl()
        self.assertEquals(1, len(references))
        self.assertEquals(doc3, references[0].getSourceObject().context)
        self.assertEquals(doc1, references[0].getTargetObject().context)
        self.assertEquals('beta', references[0].relationship)

        self.assertEquals(IUUID(doc1), adapter1.UID())
        self.assertIn('lookupObject?uuid', adapter1.reference_url())
        self.assertTrue(adapter1.hasRelationshipTo(adapter2))
        self.assertFalse(adapter1.hasRelationshipTo(adapter3))

        # This has been tested implicitly
        # self.assertEquals('x', adapter1.addReference())

        self.assertEquals(['alpha'], adapter1.getRelationships())
        
        adapter1.deleteReference(adapter2)
        self.assertFalse(adapter1.hasRelationshipTo(adapter2))

        adapter1.addReference(adapter2, relationship='alpha')
        adapter1.deleteReferences('alpha')
        self.assertFalse(adapter1.hasRelationshipTo(adapter2))
