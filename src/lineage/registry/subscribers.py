from zope.component import (
    adapter,
    getSiteManager,
)
from plone.registry.interfaces import IRegistry
from collective.lineage.interfaces import (
    IChildSiteCreatedEvent,
    IChildSiteRemovedEvent,
)
from .proxy import (
    REGISTRY_NAME,
    LineageRegistry,
)

@adapter(IChildSiteCreatedEvent)
def enableChildRegistry(event):
    child = event.object
    sm = getSiteManager(context=child)    
    if REGISTRY_NAME not in child.objectIds():
        child[REGISTRY_NAME] = LineageRegistry(REGISTRY_NAME).__of__(child)
    sm.registerUtility(component=child[REGISTRY_NAME], provided=IRegistry) 
    
@adapter(IChildSiteRemovedEvent)
def disableChildRegistry(event):
    if REGISTRY_NAME not in child.objectIds():
        return
    # we keep the registry here (intentionally)
    sm = getSiteManager(context=child)
    sm.unregisterUtility(component=child[REGISTRY_NAME], provided=IRegistry)