# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from sc.microsite.config import ADD_PERMISSION
from sc.microsite.config import PROJECTNAME
from sc.microsite.testing import INTEGRATION_TESTING
from zope.component import getAllUtilitiesRegisteredFor

import unittest


class InstallTestCase(unittest.TestCase):
    """Test package installation procedures"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_add_permission(self):
        roles = self.portal.rolesOfPermission(ADD_PERMISSION)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Manager', 'Site Administrator', 'Owner', 'Contributor']
        self.assertItemsEqual(roles, expected)

    def test_version(self):
        setup_tool = self.portal['portal_setup']
        profile = 'sc.microsite:default'
        self.assertEqual(
            setup_tool.getLastVersionForProfile(profile), (u'1001',))

    def test_hidden_products(self):
        from sc.microsite.config import HIDDEN_PRODUCTS
        packages = [p['id'] for p in self.qi.listInstallableProducts()]
        deps = set(HIDDEN_PRODUCTS)
        result = [p for p in deps if p in packages]
        self.assertFalse(
            result,
            ('These packages are still visible: {0}'.format(', '.join(result)))
        )

    def test_hidden_profiles(self):
        from sc.microsite.config import HIDDEN_PROFILES
        not_installable = []
        utils = getAllUtilitiesRegisteredFor(INonInstallable)
        for util in utils:
            not_installable.extend(util.getNonInstallableProfiles())
        profiles = set(HIDDEN_PROFILES)
        result = [p for p in profiles if p not in not_installable]
        self.assertFalse(
            result,
            ('These profiles are still visible: {0}'.format(', '.join(result)))
        )


class UninstallTestCase(unittest.TestCase):
    """Test package uninstall."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))
