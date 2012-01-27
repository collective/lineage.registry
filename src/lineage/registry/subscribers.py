from zope.component import adapter
from collective.lineage.interfaces import IChildSiteCreatedEvent
from collective.lineage.interfaces import IChildSiteRemovedEvent

@adapter(IChildSiteCreatedEvent)
def enableChildRegistry(event):
    pass

@adapter(IChildSiteRemovedEvent)
def disableChildRegistry(event):
    pass

