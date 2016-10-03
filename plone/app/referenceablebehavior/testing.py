# -*- coding: utf-8 -*-
from Products.Archetypes.atapi import (
        BaseSchema, ReferenceField, Schema, ReferenceWidget, BaseContent,
        registerType)
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent
from plone.app.testing import layers

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2
from Products.GenericSetup import EXTENSION, profile_registry

def setupSampleTypeProfile():
    profile_registry.registerProfile('Testing_sampletypes',
        'Archetypes Sample Content Types',
        'Extension profile of Archetypes sample content types',
        'profiles/sample_types',
        'plone.app.referenceablebehavior',
        EXTENSION)


class ReferenceableBehaviorLayer(PloneSandboxLayer):
    defaultBases = (
        PLONE_APP_CONTENTTYPES_FIXTURE,
    )

    def setUpZope(self, app, configurationContext):
        import Products.Archetypes
        self.loadZCML(package=Products.Archetypes)
        z2.installProduct(app, 'Products.Archetypes')
        setupSampleTypeProfile()
        import plone.app.referenceablebehavior
        self.loadZCML(package=plone.app.referenceablebehavior)
        z2.installProduct(app, 'plone.app.referenceablebehavior')

    def setUpPloneSite(self, portal):
        # install into the Plone site
        self.applyProfile(portal, 'plone.app.referenceablebehavior:default')
        self.applyProfile(portal, 'plone.app.referenceablebehavior:Testing_sampletypes')
        ttool = getToolByName(portal, 'portal_types')
        ttool.getTypeInfo('Document').behaviors += (
            'plone.app.referenceablebehavior.referenceable.IReferenceable',
        )
        setRoles(portal, TEST_USER_ID, ['Manager'])
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


class ATRefnode(BaseContent):
    """A simple archetype for testing references. It can point to itself"""

    schema = BaseSchema.copy() + Schema((
        ReferenceField('relatedItems',
            relationship='relatesTo',
            multiValued=True,
            isMetadata=True,
            languageIndependent=False,
            index='KeywordIndex',
            referencesSortable=True,
            keepReferencesOnCopy=True,
            write_permission=ModifyPortalContent,
            widget=ReferenceWidget(
                label=u'label_related_items',
                description='',
                visible={'edit': 'visible', 'view': 'invisible'}
                )
           ),   # make it a list
        )
    )


registerType(ATRefnode, 'plone.app.referenceablebehavior')
