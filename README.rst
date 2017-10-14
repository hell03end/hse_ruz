hse_ruz
=======

.. image:: https://travis-ci.org/hell03end/hse_ruz.svg?branch=master
    :target: https://travis-ci.org/hell03end/hse_ruz
.. image:: https://badge.fury.io/py/hse_ruz.svg
    :target: https://badge.fury.io/py/hse_ruz

Python wrapper for HSE RUZ API


Requirements
------------

* Python Python 3.3+ or PyPy3


Installation
------------

.. code:: bash
    pip install hse_ruz


Usage
-----

Note: add ruz api url throw `API_RUZ_URL` environment variable.

.. code:: python
    from ruz import RUZ
    api = RUZ()
    assert api.v == 2
    assert api.get("buildings")