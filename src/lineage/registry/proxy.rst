Testing the Layered Proxy Registry
==================================

Basic Setup
-----------

Create ```child``` folder for tests::

    >>> portal = layer.get('app').plone
    >>> z2.login(portal['acl_users'], 'manager')
    >>> childid = portal.invokeFactory("Folder", "child")
    >>> child = portal['child']

Make it a subsite::

    >>> from zope.component import provideUtility
    >>> from p4a.subtyper.engine import Subtyper
    >>> provideUtility(Subtyper())
    >>> from zope.component import getUtility
    >>> from p4a.subtyper.interfaces import ISubtyper
    >>> subtyper = getUtility(ISubtyper)
    >>> subtyper.change_type(child, u'collective.lineage.childsite')
    >>> from zope.component.interfaces import ISite
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

    >>> child_registry._parent_registry
    <Registry at /plone/portal_registry used for /plone/child/lineage_registry>

    >>> psm = getSiteManager(portal)    
    >>> portal_registry = psm.getUtility(IRegistry)
    >>> child_registry._parent_registry.aq_base is portal_registry.aq_base
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

