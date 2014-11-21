import unittest
import doctest

from plone.app.referenceablebehavior.testing import PLONE_APP_REFERENCEABLE_FUNCTION_TESTING
from plone.testing import layered

tests = [
    '../referenceable.rst',
    '../uidcatalog.rst',
]


def test_suite():
    return unittest.TestSuite([
        layered(
            doctest.DocFileSuite(f, optionflags=doctest.ELLIPSIS),
            layer=PLONE_APP_REFERENCEABLE_FUNCTION_TESTING
        )
        for f in tests
    ])
