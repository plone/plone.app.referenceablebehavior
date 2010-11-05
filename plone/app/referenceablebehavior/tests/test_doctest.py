import unittest

from Testing import ZopeTestCase as ztc

from plone.app.referenceablebehavior.tests.base import ReferenceableFunctionalTestCase

def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'referenceable.txt', package='plone.app.referenceablebehavior',
            test_class=ReferenceableFunctionalTestCase),

        ztc.FunctionalDocFileSuite(
            'uidcatalog.txt', package='plone.app.referenceablebehavior',
            test_class=ReferenceableFunctionalTestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
