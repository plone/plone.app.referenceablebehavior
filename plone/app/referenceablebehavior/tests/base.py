from plone.app.dexterity.tests import base as dexterity_base
from plone.app.referenceablebehavior.tests.layer import ReferenceableLayer


class ReferenceableFunctionalTestCase(dexterity_base.DexterityFunctionalTestCase):
    layer = ReferenceableLayer
