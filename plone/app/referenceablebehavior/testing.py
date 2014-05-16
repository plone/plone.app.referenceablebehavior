from Products.CMFCore.utils import getToolByName
from plone.app.testing import layers
from plone.app.testing import applyProfile
from plone.app.testing import ploneSite
from plone.testing import z2

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE


class ReferenceableBehaviorLayer(z2.Layer):
    defaultBases = (
        PLONE_APP_CONTENTTYPES_FIXTURE,
    )

    def setUp(self):
        with ploneSite() as portal:
            applyProfile(portal, 'plone.app.referenceablebehavior:default')
            ttool = getToolByName(portal, 'portal_types')
            ttool.getTypeInfo('Document').behaviors += (
                'plone.app.referenceablebehavior.referenceable.IReferenceable',
            )
            super(ReferenceableBehaviorLayer, self).setUp()
            
            portal.invokeFactory('Document', 'doc1')
            portal.invokeFactory('Document', 'doc2')
            portal.invokeFactory('Document', 'doc3')

PLONE_APP_REFERENCEABLE_FIXTURE = ReferenceableBehaviorLayer()
PLONE_APP_REFERENCEABLE_INTEGRATION_TESTING = layers.IntegrationTesting(
    bases=(PLONE_APP_REFERENCEABLE_FIXTURE, ),
    name="plone.app.referenceable:Integration"
)
PLONE_APP_REFERENCEABLE_FUNCTION_TESTING = layers.FunctionalTesting(
    bases=(PLONE_APP_REFERENCEABLE_FIXTURE, ),
    name="plone.app.referenceable:Functional"
)
