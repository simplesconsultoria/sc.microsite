# -*- coding: utf-8 -*-
from plone import api
from sc.microsite.config import PROJECTNAME

import logging

logger = logging.getLogger(PROJECTNAME)


def enable_ipublication(context):
    """Enable IPublication behavior
    """
    behavior = 'plone.app.dexterity.behaviors.metadata.IPublication'
    portal_types = api.portal.get_tool('portal_types')
    fti = portal_types['sc.microsite']
    behaviors = fti.behaviors
    if behavior not in behaviors:
        behaviors = list(behaviors)
        behaviors.append(behavior)
        fti.behaviors = tuple(behaviors)
    logger.info('IPublication behavior applied to sc.microsite')
