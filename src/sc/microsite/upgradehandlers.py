# -*- coding: utf-8 -*-
from plone import api
from sc.microsite.config import PROJECTNAME

import logging


def upgrade_to_2(context, logger=None):
    if logger is None:
        logger = logging.getLogger(PROJECTNAME)

    logger.info('Running upgrade step to version 2')
    profile = 'profile-sc.microsite:upgrade_to_2'
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runAllImportStepsFromProfile(profile)
