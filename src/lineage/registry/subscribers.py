from .utils import disableRegistry
from .utils import enableRegistry
from collective.lineage.interfaces import IChildSiteCreatedEvent
from collective.lineage.interfaces import IChildSiteRemovedEvent
from zope.component import adapter


@adapter(IChildSiteCreatedEvent)
def enableChildRegistry(event):
    enableRegistry(event.object)


@adapter(IChildSiteRemovedEvent)
def disableChildRegistry(event):
    disableRegistry(event.object)
