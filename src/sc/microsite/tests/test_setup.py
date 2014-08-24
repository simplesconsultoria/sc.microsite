# -*- coding: utf-8 -*-
from plone.testing.z2 import Browser
from Products.CMFPlone.interfaces import INonInstallable
from Products.GenericSetup.upgrade import listUpgradeSteps
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
        self.st = self.portal['portal_setup']
        self.tt = self.portal['portal_types']


class InstallTestCase(BaseTestCase):
    """Test package installation procedures"""

    def test_installed(self):
        qi = self.qi
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_version(self):
        self.assertEqual(
            self.st.getLastVersionForProfile(self.profile),
            (u'1000',)
        )

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


class TestUpgrade(BaseTestCase):
    """Test package upgrades."""

    def get_upgrade_steps(self, source, dest):
        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        source)
        steps = [step for step in upgradeSteps
                 if (step[0]['dest'] == (dest,))
                 and (step[0]['source'] == (source,))]
        return steps

    def run_upgrade(self, source, dest):
        self.st.setLastVersionForProfile(self.profile, source)
        # Get all upgrade steps
        steps = self.get_upgrade_steps(source, dest)
        # Execute them
        for step in steps:
            if isinstance(step, list):
                step = step[0]
            step['step'].doStep(self.st)

    def test_to1000_available(self):
        source, dest = ('1', '1000')
        steps = self.get_upgrade_steps(source, dest)
        self.assertEqual(len(steps), 1)

    def test_to1000_enable_ipublication(self):
        source, dest = ('1', '1000')
        behavior = 'plone.app.dexterity.behaviors.metadata.IPublication'
        fti = self.tt['sc.microsite']
        if behavior in fti.behaviors:
            # Remove behavior if it is already there
            behaviors = list(fti.behaviors)
            behaviors.remove(behavior)
            fti.behaviors = tuple(behaviors)
        self.run_upgrade(source, dest)
        # Get the fti again
        fti = self.tt['sc.microsite']
        self.assertIn(
            behavior,
            fti.behaviors
        )


class UninstallTestCase(BaseTestCase):
    """Test package uninstall."""

    def setUp(self):
        super(UninstallTestCase, self).setUp()
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))
