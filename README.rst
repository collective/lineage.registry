This package provides a plone.app.registry for Lineage subsites. It adds a
local component with a layered-/proxy-registry.

Behaviour
=========

If a value was not found in the lineage child-site registry, it is loaded from 
the parents registry.

On value set it checks if value does not exist in child-registry and if value
is different from the parent value. Then a new record based on the parent 
record is created and added to the child-registry with new value set. If it 
already exists in child-registry value is set.

On value delete it deletes only existing values in the child-registry and does 
not touch the parent registry.

Restrictions
============

Theres no editing UI for now. 

Installation
============

Just depend in your buildout on the egg ``lineage.registry``. ZCML is
loaded automagically with z3c.autoinclude.

Install it as an addon in Plone control-panel or portal_setup.

This package is written for Plone 4.1 or later.

Source Code and Contributions
=============================

If you want to help with the development (improvement, update, bug-fixing, ...)
of ``lineage.registry`` this is a great idea!

The code is located in the
`github collective <https://github.com/collective/lineage.registry>`_.

You can clone it or `get access to the github-collective
<http://collective.github.com/>`_ and work directly on the project.

Maintainer is Jens Klein and the BlueDynamics Alliance developer team. We
appreciate any contribution and if a release is needed to be done on pypi,
please just contact one of us
`dev@bluedynamics dot com <mailto:dev@bluedynamics.com>`_

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>

