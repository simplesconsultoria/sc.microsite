# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.1b2.dev0'
description = "A very basic Dexterity-based container to be used as a microsite.",
long_description = (
    open("README.rst").read() + "\n" +
    open("CONTRIBUTORS.rst").read() + "\n" +
    open("CHANGES.rst").read()
)

setup(
    name='sc.microsite',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone microsite dexterity hotsite',
    author='Simples Consultoria',
    author_email='products@simplesconsultoria.com.br',
    url='https://github.com/simplesconsultoria/sc.microsite',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['sc'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.behavior.localdiazo',
        'collective.behavior.localregistry',
        'plone.api',
        'plone.app.content',
        'plone.app.dexterity [relations]',
        'plone.app.layout',
        'plone.app.upgrade',
        'plone.dexterity',
        'plone.supermodel',
        'Products.CMFPlone >=4.3',
        'Products.CMFQuickInstallerTool',
        'Products.GenericSetup',
        'setuptools',
        'zope.i18nmessageid',
        'zope.interface',
    ],
    extras_require={
        'test': [
            'AccessControl',
            'plone.app.robotframework',  # XXX: needed by plone.app.event
            'plone.app.testing',
            'plone.testing',
            'zope.component',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
