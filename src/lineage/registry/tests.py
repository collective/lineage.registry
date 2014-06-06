from .proxy import LineageRegistry
from .proxy import REGISTRY_NAME
from .testing import LINEAGEREGISTRY_INTEGRATION_TESTING
from .utils import disableRegistry
from .utils import enableRegistry
from Products.CMFCore.utils import getToolByName
from five.localsitemanager import make_objectmanager_site
from interlude import interact
from plone.app.registry.registry import Registry
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry
from plone.testing import layered
from plone.testing import z2
from zope import schema
from zope.component import getUtility
from zope.component.hooks import setSite
from zope.component.interfaces import ISite
from zope.interface import Interface

import doctest
import pprint
import unittest


TESTFILES = [
    ('proxy.rst', LINEAGEREGISTRY_INTEGRATION_TESTING),
]

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
optionflags |= doctest.REPORT_ONLY_FIRST_FAILURE


class ITestSchema(Interface):
    """Test schema to test the registry.forInterface call.
    """
    test_attribute = schema.TextLine(default=u"test value")


class TestLineageRegistry(unittest.TestCase):
    layer = LINEAGEREGISTRY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_registry_assignment(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.oid = self.portal.invokeFactory('Folder', 'folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        folder = self.portal[self.oid]
        registry = getUtility(IRegistry)

        if not ISite.providedBy(folder):
            make_objectmanager_site(folder)

        setSite(folder)

        pc = getToolByName(folder, 'portal_catalog')
        pc.reindexObject(folder, idxs=['object_provides'])

        enableRegistry(folder)
        self.assertIn(REGISTRY_NAME, folder.objectIds())

        registry = getUtility(IRegistry)
        self.assertTrue(isinstance(registry, LineageRegistry))

        disableRegistry(folder)
        registry = getUtility(IRegistry)
        self.assertTrue(isinstance(registry, Registry))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                docfile,
                globs={'interact': interact,
                       'pprint': pprint.pprint,
                       'z2': z2,
                       },
                optionflags=optionflags,
            ),
            layer=layer,
        )
        for docfile, layer in TESTFILES
    ])
    suite.addTest(unittest.makeSuite(TestLineageRegistry))
    return suite
