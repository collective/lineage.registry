from zope.component import adapter
from zope.component import getSiteManager
from collective.lineage.interfaces import IChildSiteCreatedEvent
from collective.lineage.interfaces import IChildSiteRemovedEvent
from .registry import LayeredProxyRegistry

@adapter(IChildSiteCreatedEvent)
def enableChildRegistry(event):
    sm = getSiteManager(context=event.object)
    # create LayeredProxyRegistry (as annotation?) of event.object if not exist
    # sm.registerUtility(self, component=None, provided=None, name=u'', info=u'', 
    #                    event=True, factory=None):
    
@adapter(IChildSiteRemovedEvent)
def disableChildRegistry(event):
    sm = getSiteManager(context=event.object)
    # sm.unregisterUtility(self, component=None, provided=None, name=u'',
    #                      factory=None):    
    # we keep the annotation

