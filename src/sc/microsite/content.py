# -*- coding: utf-8 -*-
from five import grok
from plone import api
from plone.dexterity.content import Container
from sc.microsite.interfaces import IMicrosite


class Microsite(Container):
    """A microsite.
    """
    grok.implements(IMicrosite)

    def getLocallyAllowedTypes(self):
        """
        By now we allow all allowed types without constrain.
        TODO: fully implement ISelectableConstrainTypes
        """
        portal_types = api.portal.get_tool('portal_types')
        my_type = portal_types.getTypeInfo(self)
        result = portal_types.listTypeInfo()
        return [t for t in result if my_type.allowType(t.getId()) and
                t.isConstructionAllowed(self)]

    def getImmediatelyAddableTypes(self, context=None):
        """
        By now we allow all allowed types without constrain.
        TODO: fully implement ISelectableConstrainTypes
        """
        return self.getLocallyAllowedTypes()
