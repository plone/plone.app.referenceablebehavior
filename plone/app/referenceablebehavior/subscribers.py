# -*- coding: utf-8 -*-
from Products.Archetypes import config
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IReferenceable


def deleteReferences(context, event):
    """
    """
    IReferenceable(context).deleteReferences()
