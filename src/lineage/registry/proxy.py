from persistent import Persistent
from plone.app.registry import Registry
from plone.registry import Record
from plone.registry import FieldRef
from plone.registry.interfaces import IPersistentField
from plone.registry.interfaces import IRegistry
from plone.registry.registry import _Records
from zope.component import getSiteManager
from zope.component import queryUtility
from Acquisition import aq_parent

_MARKER = object()

REGISTRY_NAME = 'lineage_registry'


def get_parent_registry(base_registry):
    # first aq_parent is container, where base_registry is contained,
    # second aq_parent is a level above the local site.
    parent = aq_parent(aq_parent(base_registry))

    # get the parent's site manager
    sm = getSiteManager(context=parent)

    registry = sm.queryUtility(IRegistry)
    if registry is not None:
        return registry
    return None


class LineageRegistry(Registry):
    """Registry which proxies values from its parent registry in the local
    component stack. On set it sets values in this layered registry.
    """

    def __init__(self, id, title=None, parent=None):
        if parent:
            # We have to acquisition-wrap the registry before the
            # _LineageRecords object is set, so that it's __parent__ attribute
            # is also set to the acquisition-wrapped registry.
            self = self.__of__(parent)
        super(LineageRegistry, self).__init__(id, title)
        # pass the acquisition-wrapped LineageRegistry instance to
        # _LineageRecords
        self._records = _LineageRecords(self)

    def __getitem__(self, name):
        return self.records[name].value

    def get(self, name, default=None):
        record = self.records.get(name, _MARKER)
        if record is _MARKER:
            return default
        return record.value

    def __setitem__(self, name, value):
        if name in self.records._values:
            self.records[name].value = value
            return
        record = Record(self.records[name].field, value)
        self.records[name] = record

    def __contains__(self, name):
        return name in self.records

    @property
    def records(self):
        return self._records


class _LineageRecords(_Records, Persistent):
    """The records stored in the registry. This implements dict-like access
    to records, where as the Registry object implements dict-like read-only
    access to values.
    """

    @property
    def _parent_records(self):
        return get_parent_registry(self.__parent__).records

    def __setitem__(self, name, record):
        parval = self._parent_records._values
        if parval.get(name, _MARKER) == record.value:
            return
        super(_LineageRecords, self).__setitem__(name, record)

    def __delitem__(self, name):
        if name not in self._values:
            return
        super(_LineageRecords, self).__delitem__(name)

    def __getitem__(self, name):
        if name not in self._values:
            return self._parent_records.__getitem__(name)
        return super(_LineageRecords, self).__getitem__(name)

    def __iter__(self):
        for name in self._values.__iter__():
            yield name
        for name in self._parent_records._values.__iter__():
            if name not in self._values:
                yield name

    def has_key(self, name):
        return name in self._values\
            or name in self._parent_records._values

    def __contains__(self, name):
        return self._values.__contains__(name)\
            or self._parent_records._values.__contains__(name)

    def keys(self, min=None, max=None):
        data = set(self._values.keys(min, max))
        data.update(self._parent_records._values.keys(min, max))
        return list(data)

    def maxKey(self, key=None):
        max([self._values.maxKey(key) +
             self._parent_records._values.maxKey(key)])

    def minKey(self, key=None):
        min([self._values.minKey(key) +
             self._parent_records._values.minKey(key)])

    def _getField(self, name):
        field = self._fields.get(name, _MARKER)
        if field is _MARKER:
            return self.parents._getField(name)
        if isinstance(field, basestring):
            recordName = field
            while isinstance(field, basestring):
                recordName = field
                field = self._fields[recordName]
            field = FieldRef(recordName, field)
        return field
