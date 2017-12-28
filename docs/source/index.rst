

Petpy - Python Wrapper of the Petfinder API
===========================================

Petpy is an unofficial wrapper of the `Petfinder API <https://www.petfinder.com/developers/api-docs>`_ for
interacting with Petfinder's database and animal welfare organizations. The library uses the
`requests <http://docs.python-requests.org/en/master/>`_ package for making calls to the API.

Getting a Petfinder API Key
===========================

`Register with Petfinder <https://www.petfinder.com/developers/api-key>`_ to receive an API key which will be
used to authenticate requests made to the API.

Introduction
============

Connecting and using the Petfinder API is straightforward with petpy. The following is a simple example of
some of the usage of the petpy library.

.. code-block :: python

   import petpy

   pf = Petfinder(API_key)

   pf.breed_list('cat')

   pf.pet_getRandom()

The example starts by creating an authenticated connection to the Petfinder API which is then used to pull the
list of cat breeds available in the Petfinder database as well as a randomly selected pet record.

Contents
========

.. toctree::
   :maxdepth: 1

   api.rst
   versions.rst

Tutorials and Examples
======================

