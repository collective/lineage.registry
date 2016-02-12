Testing the Layered Proxy Registry
==================================

Basic Setup
-----------

Create ```child``` and ```childchild``` folder for tests::

    >>> portal = layer.get('app').plone
    >>> z2.login(portal['acl_users'], 'manager')
    >>> childid = portal.invokeFactory("Folder", "child")
    >>> child = portal['child']


Make it a subsite::

    >>> from zope.component.interfaces import ISite
    >>> from collective.lineage.utils import enable_childsite
    >>> enable_childsite(child)
    >>> ISite.providedBy(child)
    True


Check registry creation
-----------------------

::

    >>> from zope.component import getSiteManager
    >>> csm = getSiteManager(child)
    >>> csm
    <PersistentComponents child>

XXX: Here test is cheating: We need to check if ```getUtility(IRegistry)``` returns the childs sitemanager registry.
Well, this needs publishers traversal as far as i know.
No idea how to do this in a test.
To be done.

What actually happens is::

    >>> from zope.component.hooks import setSite
    >>> setSite(child)

An now we can go on as if we are after publishers traversal::

    >>> from zope.component import getUtility
    >>> from plone.registry.interfaces import IRegistry
    >>> sub_registry = getUtility(IRegistry)
    >>> sub_registry
    <LineageRegistry at /plone/child/lineage_registry>


Check parent
------------

Searching parent registry::

    >>> from lineage.registry.proxy import get_parent_registry
    >>> get_parent_registry(sub_registry)
    <Registry at /plone/portal_registry>

    >>> psm = getSiteManager(portal)
    >>> portal_registry = psm.getUtility(IRegistry)
    >>> get_parent_registry(sub_registry).aq_base is portal_registry.aq_base
    True


Records Read/Write
------------------

Prepare data::

    >>> from plone.registry import Record
    >>> from plone.registry.field import TextLine

    >>> portal_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(TextLine(), u"Plone")

Read from portal registry values from child registry::

    >>> sub_registry.records
    <lineage.registry.proxy.LineageRecords object at 0x...>

    >>> sub_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

Write ...::

    >>> sub_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(TextLine(), u"Plone + Lineage")


... and read back::

    >>> sub_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'

    >>> portal_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

Iter::

    >>> [_ for _ in sub_registry.records if _ == 'lineage.registry.tests.cms']
    ['lineage.registry.tests.cms']

    >>> len([_ for _ in sub_registry.records]) > 1
    True

Remove, contains, keys::

    >>> 'lineage.registry.tests.cms' in sub_registry.records.keys()
    True

    >>> del sub_registry.records['lineage.registry.tests.cms']
    >>> 'lineage.registry.tests.cms' in sub_registry.records.keys()
    True

    >>> portal_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

    >>> sub_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

    >>> del portal_registry.records['lineage.registry.tests.cms']
    >>> 'lineage.registry.tests.cms' in sub_registry.records
    False
    >>> 'lineage.registry.tests.cms' in sub_registry.records.keys()
    False

    >>> sub_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(TextLine(), u"Plone + Lineage")

    >>> 'lineage.registry.tests.cms' in sub_registry.records
    True
    >>> 'lineage.registry.tests.cms' in sub_registry.records.keys()
    True

    >>> sub_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'


Access via registry
-------------------

::

    >>> sub_registry['lineage.registry.tests.cms']
    u'Plone + Lineage'


Now a sub sub site, childchild
------------------------------

Prepare data::

    >>> portal_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(TextLine(), u"Plone")

    >>> sub_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(TextLine(), u"Plone + Lineage")


Setup childchild site::

    >>> childchildid = portal['child'].invokeFactory("Folder", "childchild")
    >>> childchild = portal['child']['childchild']

    >>> enable_childsite(childchild)
    >>> ISite.providedBy(childchild)
    True

    >>> csm = getSiteManager(childchild)
    >>> csm
    <PersistentComponents childchild>

    >>> setSite(childchild)

    >>> subsub_registry = getUtility(IRegistry)
    >>> subsub_registry
    <LineageRegistry at /plone/child/childchild/lineage_registry>
    >>> subsub_registry.title = "subsub_registry"


Read child registry values from childchild registry::

    >>> subsub_registry.records
    <lineage.registry.proxy.LineageRecords object at 0x...>

    >>> subsub_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'


Write ...::

    >>> subsub_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(TextLine(), u"Subsubsiteplone!")


... and read back::

    >>> subsub_registry.records['lineage.registry.tests.cms'].value
    u'Subsubsiteplone!'

    >>> sub_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'

    >>> portal_registry.records['lineage.registry.tests.cms'].value
    u'Plone'


Contains::

    >>> 'lineage.registry.tests.cms' in subsub_registry.records.keys()
    True


Proxy values from one layer above::

    >>> del subsub_registry.records['lineage.registry.tests.cms']
    >>> 'lineage.registry.tests.cms' in subsub_registry.records.keys()
    True

    >>> portal_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

    >>> sub_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'

    >>> subsub_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'


Proxy values from two layers above::

    >>> del sub_registry.records['lineage.registry.tests.cms']

    >>> 'lineage.registry.tests.cms' in sub_registry.records.keys()
    True

    >>> portal_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

    >>> sub_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

    >>> subsub_registry.records['lineage.registry.tests.cms'].value
    u'Plone'


Proxy for a very new key in the portal_registry::

    >>> portal_registry.records['testvalue'] = \
    ...     Record(TextLine(title=u"Portal value"), u"Only in here")

    >>> portal_registry.records['testvalue'].value
    u'Only in here'

    >>> sub_registry.records['testvalue'].value
    u'Only in here'

    >>> subsub_registry.records['testvalue'].value
    u'Only in here'


Accessing via forInterface
--------------------------

Registering the test interface::

    >>> from lineage.registry.tests import ITestSchema
    >>> portal_registry.registerInterface(ITestSchema)

Accessing the test interface::

    >>> proxy = portal_registry.forInterface(ITestSchema)
    >>> proxy.test_attribute
    u'test value'

This should also work for the sub registry::

    >>> sub_proxy = sub_registry.forInterface(ITestSchema)
    >>> sub_proxy.test_attribute
    u'test value'

And the sub sub registry::

    >>> subsub_proxy = subsub_registry.forInterface(ITestSchema)
    >>> subsub_proxy.test_attribute
    u'test value'


Test more of the LineageRecords API
-----------------------------------

Containment::

    >>> 'lineage.registry.tests.ITestSchema.test_attribute' in portal_registry
    True

    >>> 'lineage.registry.tests.ITestSchema.test_attribute' in sub_registry
    True

    >>> 'lineage.registry.tests.ITestSchema.test_attribute' in subsub_registry
    True


Has Key::

#    >>> portal_registry.records.has_key('lineage.registry.tests.ITestSchema.test_attribute')
#    True

#    >>> sub_registry.records.has_key('lineage.registry.tests.ITestSchema.test_attribute')
#    True

#    >>> subsub_registry.records.has_key('lineage.registry.tests.ITestSchema.test_attribute')
#    True


Iter::

    >>> 'lineage.registry.tests.ITestSchema.test_attribute' in [it for it in portal_registry.records]
    True

    >>> 'lineage.registry.tests.ITestSchema.test_attribute' in [it for it in sub_registry.records]
    True

    >>> 'lineage.registry.tests.ITestSchema.test_attribute' in [it for it in subsub_registry.records]
    True


Keys::

    >>> 'lineage.registry.tests.ITestSchema.test_attribute' in portal_registry.records.keys()
    True

    >>> 'lineage.registry.tests.ITestSchema.test_attribute' in sub_registry.records.keys()
    True

    >>> 'lineage.registry.tests.ITestSchema.test_attribute' in subsub_registry.records.keys()
    True


minKey::

    >>> portal_registry.records.minKey(key='lineage.registry.tests.ITestSchema.test_attribute')
    'lineage.registry.tests.ITestSchema.test_attribute'

    >>> sub_registry.records.minKey(key='lineage.registry.tests.ITestSchema.test_attribute')
    'lineage.registry.tests.ITestSchema.test_attribute'

    >>> subsub_registry.records.minKey(key='lineage.registry.tests.ITestSchema.test_attribute')
    'lineage.registry.tests.ITestSchema.test_attribute'


maxKey::

    >>> portal_registry.records.maxKey(key='lineage.registry.tests.ITestSchema.test_attribute')
    'lineage.registry.tests.ITestSchema.test_attribute'

    >>> sub_registry.records.maxKey(key='lineage.registry.tests.ITestSchema.test_attribute')
    'lineage.registry.tests.ITestSchema.test_attribute'

    >>> subsub_registry.records.maxKey(key='lineage.registry.tests.ITestSchema.test_attribute')
    'lineage.registry.tests.ITestSchema.test_attribute'


Setting over registry boundaries
================================

::

    >>> portal_registry.records['testkey'] = Record(TextLine(), u"Testval1")

    >>> sub_registry.records['testkey'] = Record(TextLine(), u"Testval1")

    >>> subsub_registry.records['testkey'] = Record(TextLine(), u"Testval1")


These settings should be available for all registries in the chain::

    >>> portal_registry.records['testkey'].value
    u'Testval1'

    >>> sub_registry.records['testkey'].value
    u'Testval1'

    >>> subsub_registry.records['testkey'].value
    u'Testval1'


... but actually only be set on portal_registry, since we have set all the same values::

    >>> portal_registry.records._values.get('testkey', False)
    u'Testval1'

    >>> sub_registry.records._values.get('testkey', False)
    False

    >>> subsub_registry.records._values.get('testkey', False)
    False


Now we're setting something different::

    >>> sub_registry.records['testkey'] = Record(TextLine(), u"Testval2")

    >>> subsub_registry.records['testkey'] = Record(TextLine(), u"Testval3")


These settings should be stored in it the registries, where they were set::

    >>> portal_registry.records['testkey'].value
    u'Testval1'

    >>> sub_registry.records['testkey'].value
    u'Testval2'

    >>> subsub_registry.records['testkey'].value
    u'Testval3'


Now for sure::

    >>> portal_registry.records._values.get('testkey', False)
    u'Testval1'

    >>> sub_registry.records._values.get('testkey', False)
    u'Testval2'

    >>> subsub_registry.records._values.get('testkey', False)
    u'Testval3'



Finally, testing _getField with records set above::

    >>> portal_registry.records._getField(name='testkey')
    <plone.registry.field.TextLine object at ...>

    >>> sub_registry.records._getField(name='testkey')
    <plone.registry.field.TextLine object at ...>

    >>> subsub_registry.records._getField(name='testkey')
    <plone.registry.field.TextLine object at ...>


Done.

::

#    >>> interact(locals())
