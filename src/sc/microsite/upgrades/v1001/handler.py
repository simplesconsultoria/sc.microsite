# -*- coding: utf-8 -*-
from plone.app.upgrade.utils import loadMigrationProfile
from sc.microsite.config import PROJECTNAME

import logging

logger = logging.getLogger(PROJECTNAME)


def apply_profile(context):
    """Execute profile to add new permission
    """
    profile = 'profile-sc.microsite.upgrades.v1001:default'
    loadMigrationProfile(context, profile)
    logger.info('Added new permission')
