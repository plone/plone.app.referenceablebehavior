import unittest
import doctest
from plone.testing import layered

from plone.app.referenceablebehavior.testing import PLONE_APP_REFERENCEABLE_FUNCTION_TESTING

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE #|
              # doctest.REPORT_ONLY_FIRST_FAILURE
               )

DOCTEST_FILES = ['referenceable.rst', 'uidcatalog.rst']

def test_suite():
   suite = unittest.TestSuite()
   for testfile in DOCTEST_FILES:
        suite.addTest(layered(
            doctest.DocFileSuite(testfile,
                                 optionflags=OPTIONFLAGS,
                                 package="plone.app.referenceablebehavior",),
            layer=PLONE_APP_REFERENCEABLE_FUNCTION_TESTING))
   return suite
