from plone.app.dexterity.tests import layer as dexterity_layer
# BBB Zope 2.12
try:
    from Zope2.App import zcml
    from OFS import metaconfigure
    zcml # pyflakes
    metaconfigure
except ImportError:
    from Products.Five import zcml
    from Products.Five import fiveconfigure as metaconfigure

class ReferenceableLayer(dexterity_layer.DexterityLayer):

    @classmethod
    def setUp(cls):
        dexterity_layer.DexterityLayer.setUp()
        metaconfigure.debug_mode = True
        import plone.app.referenceablebehavior
        zcml.load_config('configure.zcml', plone.app.referenceablebehavior)
        metaconfigure.debug_mode = False
