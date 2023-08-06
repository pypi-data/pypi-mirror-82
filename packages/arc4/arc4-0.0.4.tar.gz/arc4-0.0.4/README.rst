arc4
====

.. image:: https://travis-ci.org/manicmaniac/arc4.svg?branch=master
   :target: https://travis-ci.org/manicmaniac/arc4
   :alt: Build Status

.. image:: https://readthedocs.org/projects/arc4/badge/?version=latest
   :target: https://arc4.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

A small and insanely fast ARCFOUR (RC4) cipher implementation of Python.

* Strongly focused on performance; entire source code is written in C.
* Easily installable; single file with no dependency.

Benchmark
---------

Below is benchmark metrics against 3 major RC4 implementations.

arc4 is 67 % faster than the de facto `PyCrypto <https://pypi.org/project/pycrypto/>`_ library.
Also, 1889 % faster than pure-Python `rc4 <https://pypi.org/project/rc4/>`_ library.

========= ==============
arc4      0.332659006119
PyCrypto  0.544879198074
rc4       6.60579204559
========= ==============

The whole benchmark code is in ``./benchmark.py``.

Install
-------

Install from PyPI::

   pip install arc4

Or clone the repo and do install::

   git clone https://github.com/manicmaniac/arc4.git
   cd arc4
   python setup.py install

Usage
-----

.. code:: python

   from arc4 import ARC4

   arc4 = ARC4('key')
   cipher = arc4.encrypt('some plain text to encrypt')

Because RC4 is a stream cipher, you must initialize RC4 object in the beginning of each operations.

.. code:: python

   arc4 = ARC4('key')
   arc4.decrypt(cipher)

Testing
-------

.. code:: python

   python -m unittest discover

License
-------

This software is under the MIT License.
