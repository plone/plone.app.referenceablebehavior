from Products.Archetypes.setuphandlers import install_uidcatalog
from Products.Archetypes.setuphandlers import install_referenceCatalog


def setup_referenceablebehavior(context):
    if context.readDataFile('referenceablebehavior.txt') is None:
        return
    site = context.getSite()
    install_uidcatalog([], site)
    install_referenceCatalog([], site)
