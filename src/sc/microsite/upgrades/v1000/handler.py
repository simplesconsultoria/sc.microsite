# -*- coding:utf-8 -*-

from sc.microsite.config import PROJECTNAME

import logging


def do_upgrade(context):
    """Upgrade to version 1000
    """
    logger = logging.getLogger(PROJECTNAME)
    logger.info('Upgraded to version 1000')
