# -*- coding: utf-8 -*-
from plone.testing.z2 import Browser
from Products.CMFPlone.interfaces import INonInstallable
from sc.microsite.config import ADD_PERMISSION
from sc.microsite.config import HIDDEN_PRODUCTS
from sc.microsite.config import HIDDEN_PROFILES
from sc.microsite.config import PROJECTNAME
from sc.microsite.testing import INTEGRATION_TESTING
from zope.component import getAllUtilitiesRegisteredFor

import unittest


class BaseTestCase(unittest.TestCase):

    """Base test case for package setup tests."""

    layer = INTEGRATION_TESTING
    profile = 'sc.microsite:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']


class InstallTestCase(BaseTestCase):

    """Test package installation procedures"""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_add_permission(self):
        roles = self.portal.rolesOfPermission(ADD_PERMISSION)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Manager', 'Site Administrator', 'Owner', 'Contributor']
        self.assertItemsEqual(roles, expected)

    def test_version(self):
        setup = self.portal['portal_setup']
        self.assertEqual(
            setup.getLastVersionForProfile(self.profile), (u'1001',))

    def test_static_resource_grokker(self):
        """Grok does not register automatically the static resources anymore see:
        http://svn.zope.org/five.grok/trunk/src/five/grok/meta.py?rev=123298&r1=112163&r2=123298
        """
        portal = self.layer['portal']
        app = self.layer['app']
        browser = Browser(app)
        portal_url = portal.absolute_url()
        browser.open('%s/++resource++sc.microsite' % portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')

    def test_hidden_products(self):
        packages = [p['id'] for p in self.qi.listInstallableProducts()]
        deps = set(HIDDEN_PRODUCTS)
        result = [p for p in deps if p in packages]
        self.assertFalse(
            result,
            ('These packages are still visible: {0}'.format(', '.join(result)))
        )

    def test_hidden_profiles(self):
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


class UninstallTestCase(BaseTestCase):

    """Test package uninstall."""

    def setUp(self):
        super(UninstallTestCase, self).setUp()
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))
