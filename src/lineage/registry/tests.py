import unittest
import doctest
import pprint
from interlude import interact
from plone.testing import (
    layered,
    z2,
)
from .testing import LINEAGEREGISTRY_INTEGRATION_TESTING

TESTFILES = [
    ('proxy.rst', LINEAGEREGISTRY_INTEGRATION_TESTING),
]

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
optionflags |= doctest.REPORT_ONLY_FIRST_FAILURE

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