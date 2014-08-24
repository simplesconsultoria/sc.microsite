# -*- coding: utf-8 -*-
from collective.behavior.localdiazo.behavior import ILocalDiazo
from collective.behavior.localregistry.behavior import ILocalRegistry
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.dexterity.interfaces import IDexterityFTI
from Products.ATContentTypes.lib.constraintypes import ACQUIRE
from Products.CMFPlone.utils import _createObjectByType
from sc.microsite.interfaces import IMicrosite
from sc.microsite.testing import INTEGRATION_TESTING
from zope.component import createObject
from zope.component import queryUtility

import unittest


class CoverIntegrationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'test')

        self.m1 = api.content.create(self.folder, 'sc.microsite', 'm1')

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
        self.folder.setDefaultPage('m1')
        self.assertEqual(self.folder.default_page, 'm1')

    def test_microsite_layouts(self):
        self.assertEqual(self.m1.getAvailableLayouts(),
                         [('folder_summary_view', 'Summary view'),
                          ('folder_full_view', 'All content'),
                          ('folder_tabular_view', 'Tabular view'),
                          ('atct_album_view', 'Thumbnail view'),
                          ('folder_listing', 'Standard view')])
        self.assertEqual(self.m1.getLayout(), 'folder_listing')

    def test_microsite_constrain(self):
        self.assertEqual(self.m1.getLocallyAllowedTypes(), [])
        self.assertEqual(self.m1.getImmediatelyAddableTypes(), [])
        _createObjectByType("Folder", self.m1, 'subfolder')
        self.m1.subfolder.setConstrainTypesMode(ACQUIRE)
        self.assertEqual(self.m1.subfolder.getLocallyAllowedTypes(), [])
        self.assertEqual(self.m1.subfolder.getImmediatelyAddableTypes(), [])
