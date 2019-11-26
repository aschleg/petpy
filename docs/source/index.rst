

petpy - Python Wrapper of the Petfinder API
===========================================

Petpy is an unofficial Pythonwrapper of the `Petfinder API <https://www.petfinder.com/developers/api-docs>`_ for
interacting with Petfinder's database of animals and animal welfare organizations.

Getting a Petfinder API and Secret Key
======================================

An account must first be created with `Petfinder <https://www.petfinder.com/developers/>`_ to receive an API and secret
key. The API and secret key will be used to grant access to the Petfinder API, which lasts for 3600 seconds, or one
hour. After the authentication period ends, you must re-authenticate with the Petfinder API.

Installation
============

:code:`petpy` is best installed through :code:`pip`.

    .. code-block:: bash

        pip install petpy

For those of you who prefer it, the library can also be cloned or downloaded into a location of your choosing and then
installed using the :code:`setup.py` script per the following:

    .. code-block:: bash

       git clone git@github.com:aschleg/petpy.git
       cd petpy
       python setup.py install

Contents
========

.. toctree::
   :maxdepth: 1

   api.rst
   exceptions.rst
   versions.rst
   contributors.rst

Introduction
============

Connecting and using the Petfinder API is as straightforward as initializing the :code:`Petfinder()` class. The
following are several examples for extracting data from the Petfinder database and interacting with the Petfinder API.

Authenticating with the Petfinder API
-------------------------------------

Authentication to the Petfinder API occurs when the :code:`Petfinder()` class is initialized.

    .. code-block:: python

        import petpy
        pf = Petfinder(key=API_key, secret=API_secret)

Calls to the API to extract data can now be made!

Finding Animal Types
--------------------

    .. code-block:: python

       # All animal types and their relevant data.
       all_types = pf.animal_types()

       # Returning data for a single animal type
       dogs = pf.animal_types('dog')

       # Getting multiple animal types at once
       cat_dog_rabbit_types = pf.animal_types(['cat', 'dog', 'rabbit'])

Get Breeds of Animal Types
--------------------------

    .. code-block:: python

       cat_breeds = pf.breeds('cat')
       dog_breeds = pf.breeds('dog')

       # All available breeds or multiple breeds can also be returned.
       all_breeds = pf.breeds()
       cat_dog_rabbit = pf.breeds(types=['cat', 'dog', 'rabbit'])

The `breeds` method can also be set to coerce the returned JSON results into a pandas DataFrame by setting
the parameter `return_df = True`.

    .. code-block:: python

       cat_breeds_df = pf.breeds('cat', return_df = True)
       all_breeds_df = pf.breeds(return_df = True)

Getting animals on Petfinder
----------------------------

The :code:`animals()` method returns animals based on specified criteria that are listed in the Petfinder database.
Specific animals can be searched using the :code:`animal_id` parameter, or a search of the database can be performed
by entering the desired search criteria.

    .. code-block:: python

       # Getting first 20 results without any search criteria
       animals = pf.animals()

       # Extracting data on specific animals with animal_ids

       animal_ids = []
       for i in animals['animals'][0:3]:
           animal_ids.append(i['id'])

       animal_data = pf.animals(animal_id=animal_ids)

       # Returning a pandas DataFrame of the first 150 animal results
       animals = pf.animals(results_per_page=50, pages=3, return_df=True)

Getting animal welfare organizations in the Petfinder database
--------------------------------------------------------------

Similar to the :code:`animals()` method described above, the :code:`organizations()` method returns data on animal
welfare organizations listed in the Petfinder database based on specific criteria, if any. In addition to a general
search of animal welfare organizations, specific organizational data can be extracted by supplying the
:code:`organizations()` method with organization IDs.

    .. code-block:: python

       # Return the first 1,000 animal welfare organizations as a pandas DataFrame
       organizations = pf.organizations(results_per_page=100, pages=10, return_df=True)

       # Get organizations in the state of Washington
       wa_organizations = pf.organizations(state='WA')

Tutorials and Examples
======================

The following are Jupyter Notebooks (launched in Github) that introduce the petpy package and some examples of
its usage. The notebooks can also be launched in an `interactive environment <https://hub.mybinder.org/user/aschleg-petpy-klvuc0pp/tree/docs/notebooks>`_
with `binder <https://mybinder.org/>`_

- `Introduction to petpy <https://github.com/aschleg/petpy/blob/master/docs/notebooks/01-Introduction%20to%20petpy.ipynb>`_

Please note the following notebook is still based on the legacy version of the Petfinder API and thus are not fully
representative of the functionality and methods of the most recent version of :code:`petpy` and the Petfinder API.
These are currently being updated to reflect the new version of :code:`petpy`.

- `Download 45,000 Cat Images in 6.5 Minutes with petpy and multiprocessing <https://github.com/aschleg/petpy/blob/master/docs/notebooks/02-Download%2045%2C000%20Adoptable%20Cat%20Images%20with%20petpy%20and%20multiprocessing.ipynb>`_
