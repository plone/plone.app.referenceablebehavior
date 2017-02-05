Changelog
=========

0.7.7 (2017-02-05)
------------------

Bug fixes:

- Do not load ``plone.app.referenceablebehavior.testing`` on package registration as it adds a broken dependency to plone.app.testing.
  [hvelarde]

- Make tests pass with ZCatalog 4
  [pbauer]


0.7.6 (2016-11-09)
------------------

Bug fixes:

- Add coding header on python files.
  [gforcada]

0.7.5 (2016-08-18)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


0.7.4 (2016-02-20)
------------------

Fixes:

- Moved translations to plone.app.locales.
  Requires plone.app.locales 4.3.9 or higher.
  [claytonc]


0.7.3 (2015-09-07)
------------------

- Linkintegrity no longer uses the reference_catalog. Skip tests that assume
  that is does.
  [pbauer]


0.7.2 (2015-07-18)
------------------

- Move docs/HISTORY.txt -> CHANGES.rst.
  [timo]

- Remove superfluous 'for'.
  [fulv]


0.7.1 (2015-03-12)
------------------

- Fix tests so they run on jenkins 4.3 - ecosystem
  [maartenkling]

- Ported to plone.app.testing
  [tomgross]

0.7.0 (2014-05-21)
------------------

- Slowly reducing AT behaviors. This package still depends on
  Archetypes but does not require its GS Profile to run.
  There are two tools currently provided by AT that are now installed
  with tis profile
  [do3cc]

- Removed unused references to plone.directives.form.
  [do3cc]


0.6 (2014-04-16)
----------------

- Fix test failures due to id changes in forms.
  [vanrees]


0.5 (2013-01-10)
----------------

- Add a more complete implementation of the IReferenceable interface from
  Archetypes.  Dexterity content using this behavior is now adaptable to
  IReferenceable rather than providing it directly.
  [jpgimenez]

- Import getSite from zope.component to avoid dependency on zope.app.component.
  [hvelarde]


0.4.2 (2012-08-19)
------------------

- Get object's UID in a more proper way.
  [frapell]


0.4.1 (2012-08-18)
------------------

- Fix packaging error.
  [esteele]


0.4 (2012-08-18)
----------------

- Declare the dependency on Archetypes.
  [davisagli]

- Handle IObjectMovedEvent events for referenceable types to avoid
  "unsuccessfully attempted to uncatalog an object" errors when removing
  an object previously moved.
  [frapell]

0.3 (2011-05-18)
----------------

- Try obj first in event handlers, fall back to getSite(). When a site is being
  deleted getSite() will return None so isn't useful.
  [lentinj]

0.2 (2011-04-30)
----------------

- Use getSite() hook in event handlers, since the object may be
  not acquisition-wrapped in certain circumstances.
  [jbaumann]

- Fix broken IReferenceable import.
  [daftdog]

0.1 (2011-02-11)
----------------

- Add "locales" directory and french translation for the behavior.
  [sylvainb]

- Add referenceable behavior to dexterity
  [toutpt]

- Initial release
  [sylvainb]
