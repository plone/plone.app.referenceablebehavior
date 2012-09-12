from Products.Archetypes import config
from Products.CMFCore.utils import getToolByName


def deleteReferences(context, event):
    """
    """
    tool = getToolByName(context, config.REFERENCE_CATALOG)
    tool.deleteReferences(context.UID(), None)
    
