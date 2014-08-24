*********
Microsite
*********

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

A very basic Dexterity-based container to be used as a microsite.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/simplesconsultoria/sc.microsite.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/simplesconsultoria/sc.microsite

.. image:: https://coveralls.io/repos/simplesconsultoria/sc.microsite/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/simplesconsultoria/sc.microsite

.. image:: https://pypip.in/d/sc.microsite/badge.png
    :alt: Downloads
    :target: https://pypi.python.org/pypi/sc.microsite/

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

#. Edit your buildout.cfg and add ``sc.microsite`` to the list of eggs to
   install::

    [buildout]
    ...
    eggs =
        sc.microsite

#. If you are using Plone 4.2.x you need to add the following also::

    [versions]
    ...
    plone.app.theming = 1.1.1

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``sc.microsite`` and click the 'Activate' button.

.. Note::
	You may have to empty your browser cache and save your resource registries
	in order to see the effects of the product installation.

Usage
^^^^^

TBA.

.. _`opening a support ticket`: https://github.com/simplesconsultoria/sc.microsite/issues
