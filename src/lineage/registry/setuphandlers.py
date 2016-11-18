# -*- coding: utf-8 -*-
from collective.lineage.interfaces import IChildSite
from lineage.registry.proxy import REGISTRY_NAME
from lineage.registry.utils import disableRegistry
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'lineage.registry:uninstall',
        ]


def uninstall(context):
    """Uninstall script"""
    # query all childsites from catalog
    for brain in api.content.find(object_provides=IChildSite):
        obj = brain.getObject()
        if REGISTRY_NAME in obj:
            disableRegistry(obj)
            obj.manage_delObjects([REGISTRY_NAME])
