hse_ruz
=======

.. image:: https://travis-ci.org/hell03end/hse_ruz.svg?branch=master
    :target: https://travis-ci.org/hell03end/hse_ruz
.. image:: https://badge.fury.io/py/hse_ruz.svg
    :target: https://badge.fury.io/py/hse_ruz

Python wrapper for HSE RUZ API.

`What's new?`__

__ https://github.com/hell03end/hse_ruz/wiki/Changelog

Feel free to contribute.


Requirements
------------

* Python Python 3.3+ or PyPy3


Installation
------------

.. code-block:: bash

    pip install hse_ruz
    # or update
    pip install -U hse_ruz


Usage
-----

.. code-block:: python

    from ruz import RUZ
    api = RUZ()
    assert api.v == 1
    assert api.person_lessons("mymail@edu.hse.ru")


Contributing
------------

Please, use type annotations.

.. code-block:: bash

    git clone https://github.com/hell03end/hse_ruz.git
    cd hse_ruz
    pytest -v  # check requests schema is valid and etc.
