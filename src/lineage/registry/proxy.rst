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

    >>> from p4a.subtyper.engine import Subtyper
    >>> from p4a.subtyper.interfaces import ISubtyper
    >>> from zope.component import getUtility
    >>> from zope.component import provideUtility
    >>> from zope.component.interfaces import ISite
    >>> provideUtility(Subtyper())
    >>> subtyper = getUtility(ISubtyper)

    >>> subtyper.change_type(child, u'collective.lineage.childsite')
    >>> ISite.providedBy(child)
    True


Check registry creation
-----------------------

::

    >>> from zope.component import getSiteManager
    >>> csm = getSiteManager(child)
    >>> csm
    <PersistentComponents child>

XXX: Here test is cheating: We need to check if ```getUtility(IRegistry)```
returns the childs sitemanager registry. Well, this needs publishers traversal
as far as i know. No idea how to do this in a test. To be done.

What actually happens is::

    >>> from zope.component.hooks import setSite
    >>> setSite(child)

An now we can go on as if we are after publishers traversal::

    >>> from plone.registry.interfaces import IRegistry
    >>> child_registry = getUtility(IRegistry)
    >>> child_registry
    <LineageRegistry at /plone/child/lineage_registry>
   

Check parent
------------

Searching parent registry::

    >>> from lineage.registry.proxy import get_parent_registry
    >>> get_parent_registry(child_registry)
    <Registry at /plone/portal_registry>

    >>> psm = getSiteManager(portal)
    >>> portal_registry = psm.getUtility(IRegistry)
    >>> get_parent_registry(child_registry).aq_base is portal_registry.aq_base
    True
 

Records Read/Write
------------------

Prepare data::

    >>> from plone.registry import Record
    >>> from plone.registry import field

    >>> portal_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(field.TextLine(title=u"CMS of choice"), u"Plone")

Read from portal registry values from child registry::

    >>> child_registry.records
    <lineage.registry.proxy._LineageRecords object at 0x...>

    >>> child_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

Write ...::

    >>> child_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(field.TextLine(title=u"CMS of choice"), u"Plone + Lineage")


... and read back::

    >>> child_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'

    >>> portal_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

Iter::

    >>> [_ for _ in child_registry.records if _ == 'lineage.registry.tests.cms']
    ['lineage.registry.tests.cms']

    >>> len([_ for _ in child_registry.records]) > 1
    True

Remove, contains, keys::

    >>> 'lineage.registry.tests.cms' in child_registry.records.keys()
    True

    >>> del child_registry.records['lineage.registry.tests.cms']
    >>> 'lineage.registry.tests.cms' in child_registry.records.keys()
    True

    >>> portal_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

    >>> child_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

    >>> del portal_registry.records['lineage.registry.tests.cms']
    >>> 'lineage.registry.tests.cms' in child_registry.records
    False
    >>> 'lineage.registry.tests.cms' in child_registry.records.keys()
    False

    >>> child_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(field.TextLine(title=u"CMS of choice"), u"Plone + Lineage")

    >>> 'lineage.registry.tests.cms' in child_registry.records
    True
    >>> 'lineage.registry.tests.cms' in child_registry.records.keys()
    True

    >>> child_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'

XXX Todo: minKey, maxKey, _getField

Access via registry
-------------------

::

    >>> child_registry['lineage.registry.tests.cms']
    u'Plone + Lineage'


Now a sub sub site, childchild
------------------------------

Prepare data::

    >>> portal_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(field.TextLine(title=u"CMS of choice"), u"Plone")

    >>> child_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(field.TextLine(title=u"CMS of choice"), u"Plone + Lineage")


Setup childchild site::

    >>> childchildid = portal['child'].invokeFactory("Folder", "childchild")
    >>> childchild = portal['child']['childchild']

    >>> subtyper.change_type(childchild, u'collective.lineage.childsite')
    >>> ISite.providedBy(childchild)
    True

    >>> csm = getSiteManager(childchild)
    >>> csm
    <PersistentComponents childchild>

    >>> setSite(childchild)

    >>> childchild_registry = getUtility(IRegistry)
    >>> childchild_registry
    <LineageRegistry at /plone/child/childchild/lineage_registry>
    >>> childchild_registry.title = "childchild_registry"


Read child registry values from childchild registry::

    >>> childchild_registry.records
    <lineage.registry.proxy._LineageRecords object at 0x...>

    >>> childchild_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'


Write ...::

    >>> childchild_registry.records['lineage.registry.tests.cms'] = \
    ...     Record(field.TextLine(title=u"CMS of choice"), u"Subsubsiteplone!")


... and read back::

    >>> childchild_registry.records['lineage.registry.tests.cms'].value
    u'Subsubsiteplone!'

    >>> child_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'

    >>> portal_registry.records['lineage.registry.tests.cms'].value
    u'Plone'


Contains::

    >>> 'lineage.registry.tests.cms' in childchild_registry.records.keys()
    True


Proxy values from one layer above::

    >>> del childchild_registry.records['lineage.registry.tests.cms']
    >>> 'lineage.registry.tests.cms' in childchild_registry.records.keys()
    True

    >>> portal_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

    >>> child_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'

    >>> childchild_registry.records['lineage.registry.tests.cms'].value
    u'Plone + Lineage'


Proxy values from two layers above::

    >>> del child_registry.records['lineage.registry.tests.cms']

    >>> 'lineage.registry.tests.cms' in child_registry.records.keys()
    True

    >>> portal_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

    >>> child_registry.records['lineage.registry.tests.cms'].value
    u'Plone'

    >>> childchild_registry.records['lineage.registry.tests.cms'].value
    u'Plone'


Proxy for a very new key in the portal_registry::

    >>> portal_registry.records['testvalue'] = \
    ...     Record(field.TextLine(title=u"Portal value"), u"Only in here")

    >>> portal_registry.records['testvalue'].value
    u'Only in here'

    >>> child_registry.records['testvalue'].value
    u'Only in here'

    >>> childchild_registry.records['testvalue'].value
    u'Only in here'
