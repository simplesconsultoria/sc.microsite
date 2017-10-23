# -*- coding: utf-8 -*-
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from sc.microsite.config import ADD_PERMISSION
from sc.microsite.logger import logger


def apply_profile(context):
    """Execute profile to add new permission."""
    profile = 'profile-sc.microsite.upgrades.v1001:default'
    loadMigrationProfile(context, profile)
    logger.info('Added new permission')


def fix_add_permission_existing_microsites(context):
    """For all existing Microsites we will remove all roles
       from *sc.microsite: Add Permission*
    """
    ct = api.portal.get_tool('portal_catalog')
    results = ct.searchResults(portal_type='sc.microsite')
    for brain in results:
        o = brain.getObject()
        o.manage_permission(ADD_PERMISSION, roles=[])
    logger.info('Updated permission for {0} Microsites'.format(len(results)))
