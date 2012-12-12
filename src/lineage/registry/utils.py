from zope.component import getSiteManager
from plone.registry.interfaces import IRegistry

from .proxy import REGISTRY_NAME
from .proxy import LineageRegistry


def enableRegistry(child):
    sm = getSiteManager(context=child)
    if REGISTRY_NAME not in child.objectIds():
        child[REGISTRY_NAME] = LineageRegistry(REGISTRY_NAME).__of__(child)
    sm.registerUtility(component=child[REGISTRY_NAME], provided=IRegistry)


def disableRegistry(child):
    if REGISTRY_NAME not in child.objectIds():
        return
    # we keep the registry here (intentionally)
    sm = getSiteManager(context=child)
    sm.unregisterUtility(component=child[REGISTRY_NAME], provided=IRegistry)
