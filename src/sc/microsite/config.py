# -*- coding: utf-8 -*-
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from Products.CMFPlone import interfaces as st_interfaces
from zope.interface import implements

PROJECTNAME = 'sc.microsite'

HIDDEN_PRODUCTS = [
    'sc.microsite.upgrades.v1000',
]

HIDDEN_PROFILES = [
    'sc.microsite:uninstall',
]


class HiddenProducts(object):

    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        products = []
        products = [p for p in HIDDEN_PRODUCTS]
        return products


class HiddenProfiles(object):

    implements(st_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return HIDDEN_PROFILES
