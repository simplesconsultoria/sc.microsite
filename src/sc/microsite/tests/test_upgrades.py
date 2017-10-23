# -*- coding: utf-8 -*-
from plone import api
from Products.GenericSetup.upgrade import listUpgradeSteps
from sc.microsite.config import ADD_PERMISSION
from sc.microsite.testing import INTEGRATION_TESTING

import unittest


class TestUpgrades(unittest.TestCase):

    """Test package upgrades."""

    layer = INTEGRATION_TESTING
    profile = 'sc.microsite:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.types = self.portal['portal_types']

    def get_upgrade_steps(self, source, dest):
        upgradeSteps = listUpgradeSteps(self.setup, self.profile, source)
        steps = [s for s in upgradeSteps
                 if (s[0]['dest'] == (dest,)) and (s[0]['source'] == (source,))]
        return steps

    def run_upgrade(self, source, dest):
        self.setup.setLastVersionForProfile(self.profile, source)
        # Get all upgrade steps
        upgrade_steps = self.get_upgrade_steps(source, dest)
        # Execute them
        for steps in upgrade_steps:
            for step in steps:
                step['step'].doStep(self.setup)

    def test_to1000_available(self):
        source, dest = ('1', '1000')
        steps = self.get_upgrade_steps(source, dest)
        self.assertEqual(len(steps), 1)

    def test_to1000_enable_ipublication(self):
        source, dest = ('1', '1000')
        behavior = 'plone.app.dexterity.behaviors.metadata.IPublication'
        fti = self.types['sc.microsite']
        if behavior in fti.behaviors:
            # Remove behavior if it is already there
            behaviors = list(fti.behaviors)
            behaviors.remove(behavior)
            fti.behaviors = tuple(behaviors)
        self.run_upgrade(source, dest)
        # Get the fti again
        fti = self.types['sc.microsite']
        self.assertIn(behavior, fti.behaviors)

    def test_to1001_available(self):
        source, dest = ('1000', '1001')
        steps = self.get_upgrade_steps(source, dest)
        self.assertEqual(len(steps), 1)

    def test_to1001_rolemap(self):
        source, dest = ('1000', '1001')
        self.run_upgrade(source, dest)
        roles = self.portal.rolesOfPermission(ADD_PERMISSION)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Manager', 'Site Administrator', 'Owner', 'Contributor']
        self.assertItemsEqual(roles, expected)

    def test_to1001_fix_permission(self):
        with api.env.adopt_roles(['Manager']):
            microsite = api.content.create(self.portal, 'sc.microsite', 'foo')
        # simulate state at previous version
        microsite.manage_permission(ADD_PERMISSION, roles=['Manager'])
        # run upgrade step and verify no rol is assigned to add permission
        source, dest = ('1000', '1001')
        self.run_upgrade(source, dest)
        roles = microsite.rolesOfPermission(ADD_PERMISSION)
        roles = [r['name'] for r in roles if r['selected']]
        self.assertEqual(roles, [])
