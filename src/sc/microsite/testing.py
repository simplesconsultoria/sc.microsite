# -*- coding: utf-8 -*-
"""Prepare test fixtures."""
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.z2 import ZSERVER_FIXTURE


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import sc.microsite
        self.loadZCML(package=sc.microsite)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'sc.microsite:default')

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='sc.microsite:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, ZSERVER_FIXTURE,),
    name='sc.microsite:Functional',
)
