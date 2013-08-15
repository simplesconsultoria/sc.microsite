# -*- coding: utf-8 -*-

from five import grok
from plone.dexterity.content import Container
from sc.microsite.interfaces import IMicrosite


class Microsite(Container):
    """A microsite.
    """
    grok.implements(IMicrosite)
