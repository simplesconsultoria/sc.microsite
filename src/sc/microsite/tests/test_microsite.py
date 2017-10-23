# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from collective.behavior.localdiazo.behavior import ILocalDiazo
from collective.behavior.localregistry.behavior import ILocalRegistry
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.dexterity.interfaces import IDexterityFTI
from sc.microsite.interfaces import IMicrosite
from sc.microsite.testing import INTEGRATION_TESTING
from sc.microsite.testing import IS_PLONE_5
from zope.component import createObject
from zope.component import queryUtility

import unittest


class MicrositeIntegrationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.m1 = api.content.create(self.portal, 'sc.microsite', 'm1')

    def test_adding(self):
        self.assertTrue(IMicrosite.providedBy(self.m1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='sc.microsite')
        self.assertNotEqual(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='sc.microsite')
        schema = fti.lookupSchema()
        self.assertEqual(IMicrosite, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='sc.microsite')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IMicrosite.providedBy(new_object))

    def test_exclude_from_navigation_behavior(self):
        self.assertTrue(IExcludeFromNavigation.providedBy(self.m1))

    def test_localdiazo_behavior(self):
        self.assertTrue(ILocalDiazo.providedBy(self.m1))

    def test_localregistry_behavior(self):
        self.assertTrue(ILocalRegistry.providedBy(self.m1))

    def test_navigation_root_behavior(self):
        self.assertTrue(INavigationRoot.providedBy(self.m1))

    def test_microsite_selectable_as_folder_default_view(self):
        self.portal.setDefaultPage('m1')
        self.assertEqual(self.portal.default_page, 'm1')

    def test_microsite_default_layout(self):
        self.assertEqual(self.m1.getLayout(), 'folder_listing')

    def test_microsite_available_layouts(self):
        available_layouts = self.m1.getAvailableLayouts()
        self.assertEqual(len(available_layouts), 5)

    def test_microsite_allowed_types(self):
        allowed_types = self.m1.getLocallyAllowedTypes()
        if IS_PLONE_5:
            # Plone 5 includes Collection also
            self.assertEqual(len(allowed_types), 8)
        else:
            self.assertEqual(len(allowed_types), 7)

    def test_microsite_addable_types(self):
        addable_types = self.m1.getImmediatelyAddableTypes()
        if IS_PLONE_5:
            # Plone 5 includes Collection also
            self.assertEqual(len(addable_types), 8)
        else:
            self.assertEqual(len(addable_types), 7)

    def test_can_not_add_microsite_inside_microsite(self):
        with self.assertRaises(Unauthorized):
            api.content.create(self.m1, 'sc.microsite', 'foo')
