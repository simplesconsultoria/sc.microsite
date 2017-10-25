Changelog
---------

There's a frood who really knows where his towel is.

1.1b1 (2017-10-25)
^^^^^^^^^^^^^^^^^^

- Remove dependency on five.grok.
  [rodfersou]

- Fix package dependencies.
  [hvelarde]

- Drop support for Python 2.6 and Plone 4.2.
  [hvelarde]


1.0b4 (2014-09-12)
^^^^^^^^^^^^^^^^^^

- An new permission ``sc.microsite: Add Microsite`` and an event subscriber are now provided to avoid the creation of a microsite inside another microsite.
  An upgrade step to fix existing microsites is also available.
  [ericof]


1.0b3 (2014-08-25)
^^^^^^^^^^^^^^^^^^

- Improve setup testing
  [ericof]

- Enable ``IPublication`` behavior by default to add effective date and expiration date fields to the Microsite content type.
  [hvelarde]


1.0b2 (2013-08-23)
^^^^^^^^^^^^^^^^^^

- Basic ISelectableConstrainTypes support. [jpgimenez]

- Update view methods, sc.microsite content has the same methods than a
  folder. [jpgimenez]

- Default view changed to folder_listing. [jpgimenez]

- A microsite must have INavigationRoot behavior enabled.
  [agnogueira, cleberjsantos]


1.0b1 (2013-08-15)
^^^^^^^^^^^^^^^^^^

- Initial release.
