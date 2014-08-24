# -*- coding: utf-8 -*-
"""Prepare test fixtures; note that in Plone >= 5.0 we need to manually
install the desired content types.
"""
from plone import api
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.z2 import ZSERVER_FIXTURE

PLONE_VERSION = api.env.plone_version()


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if PLONE_VERSION >= '5.0':
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)

        import sc.microsite
        self.loadZCML(package=sc.microsite)

    def setUpPloneSite(self, portal):
        if PLONE_VERSION >= '5.0':
            self.applyProfile(portal, 'plone.app.contenttypes:default')

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
