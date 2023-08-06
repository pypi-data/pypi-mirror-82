pandas-msgpack
==============

|Travis Build Status| 

**pandas-msgpack** is a package providing an interface to msgpack from pandas

In 2019, pandas deprecated the msgpack io interface,
suggesting people use pyarrow instead.

Unfortunatly, pyarrow doesn't do columns-containing-tuples,
and we do have older msgpacked DataFrames that we still need to unpack.

Somebody had already forked the msgpack code earlier, 
but it had bitrotted away from the current pandas internal.

This fork restores it to mostly-working order - notably,
all datetime and sparse array handling have been removed.
Datetime, because the numpy dtype no longer stores timezones,
and it wasn't important to our particular mission,
and sparse arrays because they have been deprecated anyway
(and were not important to our mission).


Installation
------------

Install latest development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ pip install mbf_pandas


Usage
-----

See the `pandas-msgpack documentation <https://pandas-msgpack.readthedocs.io/>`_ for more details,
just replace all :code:`import pandas_msgpack` with :code:`import mbf_pandas_msgpack`

.. |Travis Build Status| image:: https://travis-ci.org/TyberiusPrime/pandas-msgpack.svg?branch=master
   :target: https://travis-ci.org/TyberiusPrime/pandas-msgpack
