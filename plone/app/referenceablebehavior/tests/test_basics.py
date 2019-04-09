# -*- coding: utf-8 -*-
from Products.Archetypes.interfaces import IReferenceable
from Products.Archetypes.interfaces import referenceable
from plone.app.referenceablebehavior.testing import PLONE_APP_REFERENCEABLE_FUNCTION_TESTING
from plone.app.textfield import RichTextValue
from plone.uuid.interfaces import IUUID
from zope.lifecycleevent import modified
import unittest


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

    @unittest.skip('Needs Refactor. Linkintegrity does not use ref_catalog')
    def test_rename_updates_ref_catalog(self):
        doc1 = self.portal['doc1']
        doc2 = self.portal['doc2']
        ref_catalog = self.portal.reference_catalog
        doc1.text = RichTextValue('<a href="doc2">doc2</a>')
        modified(doc1)
        self.assertEquals(1, len(ref_catalog()))

        self.assertEquals([doc2], IReferenceable(doc1).getReferences())
        ref_brain = ref_catalog()[0]
        self.assertTrue(ref_brain.getPath().startswith('doc1'))
        self.portal.manage_renameObject(id='doc1', new_id='new_name')
        modified(doc1)
        self.assertEquals(1, len(ref_catalog()))
        ref_brain = ref_catalog()[0]
        self.assertTrue(ref_brain.getPath().startswith('new_name'))
        self.assertEquals([doc2], IReferenceable(doc1).getReferences())

    @unittest.skip('Needs Refactor. Linkintegrity does not use ref_catalog')
    def test_remove_cleans_ref_catalog(self):
        doc1 = self.portal['doc1']
        doc1.text = RichTextValue('<a href="doc1">doc1</a>')
        modified(doc1)
        ref_catalog = self.portal.reference_catalog
        self.assertEquals(1, len(ref_catalog()))

        self.portal.manage_delObjects(['doc1'])
        self.assertEquals(0, len(ref_catalog()))

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
        self.assertTrue('lookupObject?uuid' in adapter1.reference_url())
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
