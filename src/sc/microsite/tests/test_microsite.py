# -*- coding: utf-8 -*-

from collective.behavior.localdiazo.behavior import ILocalDiazo
from collective.behavior.localregistry.behavior import ILocalRegistry
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from sc.microsite.interfaces import IMicrosite
from sc.microsite.testing import INTEGRATION_TESTING
from zope.component import createObject
from zope.component import queryUtility

import unittest


class CoverIntegrationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('sc.microsite', 'm1')
        self.m1 = self.folder['m1']

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
