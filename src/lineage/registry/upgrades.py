from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from collective.lineage.interfaces import IChildSite
from lineage.registry.proxy import LineageRecords
from lineage.registry.proxy import REGISTRY_NAME
from lineage.registry.proxy import _LineageRecords
from zope.component.hooks import getSite
import logging

log = logging.getLogger(__name__)


def upgrade_from_persistent(context):
    portal = getSite()
    catalog = getToolByName(portal, 'portal_catalog')
    query = {}
    query['object_provides'] = IChildSite.__identifier__
    results = catalog(**query)
    log.info('There are {0} in total, stating migration...'.format(
        len(results)))

    for result in sorted(results, key=lambda it: it.getURL()):
        obj = result.getObject()
        reg = getattr(obj, REGISTRY_NAME, None)
        if reg:
            log.info('migration for {0}'.format(reg.getPhysicalPath()))
            reg = aq_base(reg)
            if not getattr(reg, '__parent__', False):
                log.info('set registry parent')
                # set the parent persitently
                reg.__parent__ = obj

            if not getattr(reg._records, '__parent__', False):
                log.info('set records parent')
                reg._records.__parent__ = reg

            if isinstance(reg._records, _LineageRecords):
                log.info('migrate records')
                oldrecs = reg._records
                reg._records = LineageRecords(reg)

                for key, val in oldrecs.items():
                    try:
                        reg._records[key] = val
                    except KeyError:
                        # just have to. maybe this is the normal case.
                        #
                        # val.value raises KeyError, val._value not.
                        # all because of
                        # plone.registry.record.Record._get_value
                        del val.__parent__
                        reg._records[key] = val
                    except:
                        log.warn('could migrate {0} for {1}'.format(key, reg))

        else:
            log.warn('could not migrate {0}'.format(reg.getPhysicalPath()))
