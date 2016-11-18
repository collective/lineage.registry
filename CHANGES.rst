
History
=======

1.4.0 (2016-11-18)
------------------

- Uninstall added. Attention: Uninstal deletes local registry!
  [jensens]


1.3.3 (2016-04-19)
------------------

- Fix: Return keys sorted, because ``RecordsProxyCollection`` expects them ordered.
  One effect fixed is that resoruce bundles in subsites are not delivered 11 to 10 times.
  [jensens]


1.3.1 (2016-02-25)
------------------

- Add profile to properly register the upgrade step.
  [thet]


1.3 (2015-07-15)
----------------

- Fix Database Conflict Errors, due to missing ``__parent__`` parameter on the
  LineageRegistry object, which led to writing it on each request. An upgrade
  step is provided. Please note, the upgrade step is bound to the
  ``collective.lineage`` profile, as we don't have a profile in here.
  [thet]


1.2 (2014-06-06)
----------------

- Fix lineage.registry for sub-subsites and other arbitrary nested sites.
  [thet]

- Added enableRegistry and disableRegistry in order to make event subscribers
  simpler. Now you can enable a local Registry in a simple folder and not only
  on collective.lineage.content.ChildFolder. See: tests.TestLineageRegistry
  [gborelli]


1.1 (2014-01-30)
----------------

- Fix bug when disabling a lineage site.
  [thet]


1.0.1
-----

- Wrong information in README.rst corrected.
  [jensens]


1.0
---

- Make it work [jensens, 2012-01-25]
