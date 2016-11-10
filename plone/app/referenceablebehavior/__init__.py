# -*- coding: utf-8 -*-
import os
import zope.i18nmessageid
MessageFactory = zope.i18nmessageid.MessageFactory("plone.app.referenceablebehavior")

PKG_NAME = "plone.app.referenceablebehavior"

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    if 'ZOPETESTCASE' in os.environ:   # register demo type only when testing
        from Products.CMFCore import utils
        from Products.CMFCore import permissions
        from Products.Archetypes.ArchetypeTool import process_types, listTypes

        content_types, constructors, ftis = process_types(
            listTypes(PKG_NAME), PKG_NAME)

        utils.ContentInit(
            '%s Content' % PKG_NAME,
            content_types=content_types,
            permission=permissions.AddPortalContent,
            extra_constructors=constructors,
            fti=ftis,
            ).initialize(context)
