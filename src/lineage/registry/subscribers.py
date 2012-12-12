from zope.component import adapter

from collective.lineage.interfaces import (
    IChildSiteCreatedEvent,
    IChildSiteRemovedEvent,
)

from .utils import enableRegistry
from .utils import disableRegistry


@adapter(IChildSiteCreatedEvent)
def enableChildRegistry(event):
    enableRegistry(event.object)


@adapter(IChildSiteRemovedEvent)
def disableChildRegistry(event):
    disableRegistry(event.object)
