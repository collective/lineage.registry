from zope.component import getSiteManager
from plone.app.registry import Registry

_MARKER = object()

class LayeredProxyRegistry(Registry):
    """Registry which proxies values from its parent registry in the local 
    component stack. On set it sets values in this registry.   
    """
    
    @property
    def _parent_registry(self):        
        sm = getSiteManager(context=self)
        import pdb;pdb.set_trace()
        raise NotImplementedError('_parent_registry')         
    
    def __getitem__(self, name):
        try:
            return self.records._values[name]
        except KeyError, e:
            return self._parent_registry[name]
    
    def get(self, name, default=None):        
        value = self.records._values.get(name, _MARKER)
        if value is _MARKER:
            value = self._parent_registry.get(name, default)
        return value
    
    def __setitem__(self, name, value):
        self.records[name].value = value
    
    def __contains__(self, name):
        return name in self.records._values or name in self._parent_registry