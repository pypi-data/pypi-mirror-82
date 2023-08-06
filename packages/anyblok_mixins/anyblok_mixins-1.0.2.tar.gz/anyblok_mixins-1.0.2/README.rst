.. This file is a part of the AnyBlok project
..
..    Copyright (C) 2014 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. image:: https://img.shields.io/pypi/v/anyblok_mixins.svg
   :target: https://pypi.python.org/pypi/anyblok/
   :alt: Version status

.. image:: https://travis-ci.org/AnyBlok/anyblok_mixins.svg?branch=master
    :target: https://travis-ci.org/AnyBlok/anyblok_mixins
    :alt: Build status

.. image:: https://coveralls.io/repos/github/AnyBlok/anyblok_mixins/badge.svg?branch=master
    :target: https://coveralls.io/github/AnyBlok/anyblok_mixins?branch=master
    :alt: Coverage
   
.. image:: https://readthedocs.org/projects/anyblok_mixins/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://anyblok-mixins.readthedocs.io/en/latest/?badge=latest

.. image:: https://badges.gitter.im/AnyBlok/community.svg
    :alt: gitter
    :target: https://gitter.im/AnyBlok/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. image:: https://img.shields.io/pypi/pyversions/anyblok_mixins.svg?longCache=True
    :alt: Python versions

AnyBlok
=======

Add some mixins to help implementation of business models

+----------------------+--------------------+---------------------------------------------------+
| Blok                 | Dependencies       | Description                                       |
+======================+====================+===================================================+
| **anyblok-mixins**   |                    | Add some Mixins to help developpers :             |
|                      |                    |                                                   |
|                      |                    | * IdColumn : add primary key id                   |
|                      |                    | * UuidColumn : add primary key uuid               |
|                      |                    | * TrackModel : add create_date and edit_date      |
|                      |                    | * ForbidUpdate : Forbid all update on a Model     |
|                      |                    | * ForbidDelete : Forbid all delete on a Model     |
|                      |                    | * Readonly : Forbid all delete and update on a    |
|                      |                    |   Model                                           |
|                      |                    | * ConditionalForbidUpdate : Need to overwrite the |
|                      |                    |   method check_if_forbid_update_condition_is_true |
|                      |                    | * ConditionalForbidDelete : Need to overwrite the |
|                      |                    |   method check_if_forbid_delete_condition_is_true |
|                      |                    | * ConditionalReadonly : Need to overwrite the     |
|                      |                    |   method check_if_forbid_update_condition_is_true | 
|                      |                    |   and check_if_forbid_delete_condition_is_true    |
|                      |                    | * BooleanForbidUpdate : add forbid_update column  |
|                      |                    | * BooleanForbidDelete : add forbid_delete column  |
|                      |                    | * BooleanReadonly : add readonly column           |
|                      |                    | * StateReadOnly : Need to overwrite the           |
|                      |                    |   method check_if_forbid_update_condition_is_true | 
|                      |                    |   and check_if_forbid_delete_condition_is_true    |
+----------------------+--------------------+---------------------------------------------------+
| **anyblok-workflow** | **anyblok-mixins** | Add Workflow behaviour                            |
+----------------------+--------------------+---------------------------------------------------+

AnyBlok / Pyramid is released under the terms of the `Mozilla Public License`.

See the `latest documentation <https://anyblok-mixins.readthedocs.io/en/latest/>`_

Running Tests
-------------

To run framework tests with ``pytest``::

    pip install pytest
    ANYBLOK_DATABASE_DRIVER=postgresql ANYBLOK_DATABASE_NAME=test_anyblok py.test anyblok_mixins/tests

AnyBlok is tested continuously using `Travis CI
<https://travis-ci.org/AnyBlok/anyblok_mixins>`_

Author
------

Jean-Sébastien Suzanne

Contributors
------------

* Jean-Sébastien Suzanne
* Pierre Verkest
* Hugo Quezada

Bugs
----

Bugs and features enhancements to AnyBlok should be reported on the `Issue
tracker <https://github.com/AnyBlok/anyblok_mixins/issues>`_.
