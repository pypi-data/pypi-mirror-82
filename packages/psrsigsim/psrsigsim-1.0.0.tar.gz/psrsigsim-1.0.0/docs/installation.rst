.. highlight:: shell

============
Installation
============


Stable release
--------------

To install PsrSimSig, run this command in your terminal:

.. code-block:: console

    $ pip install psrsigsim

This is the preferred method to install PsrSimSig, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

If you have issues with the `fitsio` installation and you already have `cfitsio`
installed you may need to reinstall or `reconfigure`_ with different flags.

.. _reconfigure: https://heasarc.gsfc.nasa.gov/docs/software/fitsio/c/c_user/node9.html

From sources
------------

The sources for PsrSimSig can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/psrsigsim/psrsigsim

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/psrsigsim/psrsigsim/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/psrsigsim/psrsigsim
.. _tarball: https://github.com/psrsigsim/psrsigsim/tarball/master
