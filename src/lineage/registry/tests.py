from .testing import LINEAGEREGISTRY_INTEGRATION_TESTING
from interlude import interact
from plone.testing import layered
from plone.testing import z2
from zope import schema
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
    return suite
