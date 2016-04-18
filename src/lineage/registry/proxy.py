from Acquisition import aq_parent
from persistent import Persistent
from plone.app.registry import Registry
from plone.registry import FieldRef
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from plone.registry.registry import _Records
from zope.component import getSiteManager
import warnings

_MARKER = object()
REGISTRY_NAME = 'lineage_registry'


def get_parent_registry(base_registry):
    # aq_parent returns the container, where the base_registry is contained
    parent = aq_parent(base_registry)

    # get the parent's site manager
    # If parent is None for pre lineage.registry 1.1 sites, return the current
    # site.
    sm = getSiteManager(context=parent)

    for base in sm._getBases():
        registry = base.queryUtility(IRegistry)
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
            # LineageRecords object is set, so that it's __parent__ attribute
            # is also set to the acquisition-wrapped registry.
            self.__parent__ = parent
        else:
            raise AssertionError(
                "parent must not be None, otherwise the Acquisition context "
                "of LineageRegistry cannot be set")

        self.id = id
        self.title = title

        # pass the acquisition-wrapped LineageRegistry instance to
        # LineageRecords
        self._records = LineageRecords(self)

    def __getitem__(self, name):
        return self.records[name].value

    def get(self, name, default=None):
        record = self.records.get(name, _MARKER)
        if record is _MARKER:
            return default
        return record.value

    def __setitem__(self, name, value):
        records = self.records
        if name in records._values:
            records[name].value = value
            return
        record = Record(records[name].field, value)
        records[name] = record

    def __contains__(self, name):
        return name in self.records

    @property
    def records(self):
        return self._records


class LineageRecords(_Records):
    """The records stored in the registry. This implements dict-like access
    to records, where as the Registry object implements dict-like read-only
    access to values.
    """

    @property
    def _parent_records(self):
        registry = get_parent_registry(self.__parent__)
        records = registry.records
        return records

    def __setitem__(self, name, record):
        parent_rec = self._parent_records.get(name, _MARKER)
        if parent_rec is not _MARKER and parent_rec.value == record.value:
            return
        super(LineageRecords, self).__setitem__(name, record)

    def __delitem__(self, name):
        if name not in self._values:
            return
        super(LineageRecords, self).__delitem__(name)

    def __getitem__(self, name):
        if name not in self._values:
            return self._parent_records.__getitem__(name)
        return super(LineageRecords, self).__getitem__(name)

    def __iter__(self):
        for name in self._values.__iter__():
            yield name
        for name in self._parent_records.__iter__():
            if name not in self._values:
                yield name

    def has_key(self, name):
        return name in self._values\
            or name in self._parent_records

    def __contains__(self, name):
        return self._values.__contains__(name)\
            or self._parent_records.__contains__(name)

    def keys(self, min=None, max=None):
        data = set(self._values.keys(min, max))
        data.update(self._parent_records.keys(min, max))
        return list(sorted(data))

    def maxKey(self, key=None):
        keys = []
        keys.append(self._parent_records.maxKey(key))
        try:
            own = self._values.maxKey(key)
            keys.append(own)
        except ValueError:
            pass
        return max(keys)

    def minKey(self, key=None):
        keys = []
        keys.append(self._parent_records.minKey(key))
        try:
            own = self._values.minKey(key)
            keys.append(own)
        except ValueError:
            pass
        return min(keys)

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


class _LineageRecords(LineageRecords, Persistent):
    """BBB: This used to be the class for the _records attribute of the
    registry. Having this be a Persistent object was always a bad idea. We
    keep it here so that we can migrate to the new structure, but it should
    no longer be used.
    """

    def __init__(self, parent):
        warnings.warn("The Records persistent class is deprecated and should not be used.", DeprecationWarning)  # noqa
        super(_LineageRecords, self).__init__(parent)
