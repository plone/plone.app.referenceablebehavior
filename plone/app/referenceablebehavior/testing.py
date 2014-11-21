from Products.CMFCore.utils import getToolByName
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_MIGRATION_FIXTURE
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import applyProfile
from plone.app.testing import layers
from plone.app.testing import setRoles
from plone.dexterity.fti import DexterityFTI
from zope.configuration import xmlconfig


class ReferenceableBehaviorLayer(PloneSandboxLayer):
    defaultBases = (
        PLONE_APP_CONTENTTYPES_MIGRATION_FIXTURE,
    )

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity
        xmlconfig.file('configure.zcml', plone.app.dexterity,
                       context=configurationContext)
        # load ZCML
        import plone.app.referenceablebehavior
        xmlconfig.file('configure.zcml', plone.app.referenceablebehavior,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.dexterity:default')
        applyProfile(portal, 'plone.app.referenceablebehavior:default')
        #ttool = getToolByName(portal, 'portal_types')
        #ttool.getTypeInfo('Document').behaviors += (
        #    'plone.app.referenceablebehavior.referenceable.IReferenceable',
        #)

        #portal.invokeFactory('Document', 'doc1')
        #portal.invokeFactory('Document', 'doc2')
        #portal.invokeFactory('Document', 'doc3')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        fti = DexterityFTI('referenceabledocument')
        portal.portal_types._setObject('referenceabledocument', fti)
        fti.klass = 'plone.dexterity.content.Item'
        fti.behaviors = (
            'plone.app.referenceablebehavior.referenceable.IReferenceable',
        )

        portal.invokeFactory('referenceabledocument', 'doc1')
        portal.invokeFactory('referenceabledocument', 'doc2')
        portal.invokeFactory('referenceabledocument', 'doc3')


PLONE_APP_REFERENCEABLE_FIXTURE = ReferenceableBehaviorLayer()
PLONE_APP_REFERENCEABLE_INTEGRATION_TESTING = layers.IntegrationTesting(
    bases=(PLONE_APP_REFERENCEABLE_FIXTURE, ),
    name="plone.app.referenceable:Integration"
)
PLONE_APP_REFERENCEABLE_FUNCTION_TESTING = layers.FunctionalTesting(
    bases=(PLONE_APP_REFERENCEABLE_FIXTURE, ),
    name="plone.app.referenceable:Functional"
)
