# coding: utf-8
import logging
from Products.CMFCore.utils import getToolByName
from .config import PROJECTNAME


def upgrade_to_2(context, logger=None):
    if logger is None:
        logger = logging.getLogger(PROJECTNAME)

    logger.info('Running upgrade profile to 2')
    profile = 'profile-sc.microsite:upgrade_to_2'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(profile)
