.. _versions:

Version History
===============

Changelog and version changes made with each release.


Version 2.0.2
-------------

Minor bug fix release with following:
  - :code:`breeds()` method now correctly returns data when a single animal type is supplied.
  - :code:`animals()` method now properly displays the correct error message when the :code:`distance` parameter is
    0 <= distance <= 500.

Version 2.0.1
-------------

- Fixes the :code:`animals()` and :code:`organizations()` method to return all matching search results when the
  :code:`pages` parameter is set to :code:`None`.
- The resulting JSON (dictionary) from the :code:`breeds()` method when the parameter :code:`return_df=False` will now
  consistently have :code:`types` as the key. Prior to this change, if the :code:`breeds()` method was called with a
  single animal type, the resulting key name in the returned object would be named :code:`type`, whereas if more than
  one animal type is specified the key name would be :code:`types`.
- The :code:`distance` parameter for the :code:`animals()` and :code:`organizations()` parameters will now raise a
  :code:`ValueError` if it is less than 0.

Version 2.0.0
-------------

New major release coinciding with the release of `v2.0 of the Petfinder API <https://www.petfinder.com/developers/>`_!
The legacy version of the Petfinder API, v1.0, will be retired in January 2020, therefore, the :code:`petpy` library has
been updated almost from the ground up to be compatible as possible with the new version of the Petfinder API! The
new version of the Petfinder API is a huge improvement over the legacy version, with many changes and additions to
the design of the API itself. As such, several methods from earlier releases of :code:`petpy` that wrapped these
endpoints will be deprecated over the next few releases.

Below is a summary of all the changes made in the release of :code:`petpy 2.0`.

- :code:`petpy` now supports the latest release of Python 3.7
- Support for Python 2.7 is discontinued as Python 2.7 will be officially discontinued in January 2020.
- The following methods have been added to :code:`petpy` to make it compatible with v2.0 of the Petfinder API.
    - :code:`animal_types()` is used to getting animal types (or type) available from the Petfinder API. The release
      of v2.0 of the Petfinder API added several endpoints for accessing animal types in the Petfinder database.
      This method wraps both Petfinder API endpoints for getting animal types. More information on the animal type
      endpoints in the Petfinder API can be found in its documentation:
      - `Get Animal Types <https://www.petfinder.com/developers/v2/docs/#get-animal-types>`_
      - `Get Single Animal Type <https://www.petfinder.com/developers/v2/docs/#get-a-single-animal-type>`_
    - :code:`breeds()` is the new method for getting available animal breeds from the Petfinder database. The API
      endpoint documentation is available on the Petfinder API documentation page.
      - `Get Animal Breeds <https://www.petfinder.com/developers/v2/docs/#get-animal-breeds>`_
    - :code:`animals()` is the method for extracting animal data available on the Petfinder API and deprecates the
      :code:`pets()` related methods. The method wraps both the :code:`animals` and :code:`animal/{id}` endpoints of
      the Petfinder API. The documentation for these endpoints can be found in the Petfinder API documentation:
      - `Get Animal <https://www.petfinder.com/developers/v2/docs/#get-animal>`_
      - `Get Animals <https://www.petfinder.com/developers/v2/docs/#get-animals>`_
    - :code:`organizations()` is now the method for extracting animal welfare organization data available on Petfinder
      and deprecates previous :code:`shelter()` related methods and endpoints. The :code:`organizations()` method wraps
      both the Petfinder API :code:`organizations` and :code:`organizations/{id}` endpoints. The Petfinder API
      documentation for these two endpoints can be found below:
      - `Get Organizations <https://www.petfinder.com/developers/v2/docs/#get-organizations>`_
      - `Get Organization <https://www.petfinder.com/developers/v2/docs/#get-organization>`_
- The following methods have been removed as they are no longer valid endpoints with the release of v2.0 of the
  PetFinder API.
  - :code:`pet_get_random()`
  - :code:`shelter_list_by_breed()`
  - :code:`shelter_get_pets()`
- General refactoring and code clean-up.

Version 1.8.2
-------------

- Add :code:`pandas` back as an installation requirement as it is included in top-level imports. :code:`pandas` is
  still not necessary to use the primary functionality of :code:`petpy`.

Version 1.8.1
-------------

- Implement check to make sure :code:`count` parameter is not larger than 1,000 records (per the Petfinder API
  limits). If :code:`count` exceeds 1,000 a :code:`ValueError` is raised.
- Add check for ensuring the number of total records to return does not exceed 2,000 when paging results with
  the :code:`pages` and :code:`count` parameters. If the desired amount of records is higher than 2,000, a
  :code:`ValueError` is raised.
- Remove Python 3.3 support. Although :code:`petpy` should work fine for those still using Python 3.3, testing for 3.3
  has been discontinued.

Version 1.8.0
-------------

- General refactoring of the :code:`petpy` library to remove unneeded methods from being exposed when importing the
  library. The best way to import and begin using :code:`petpy` is :code:`from petpy import Petfinder` or, less
  optimally, :code:`import petpy`, then calling the :code:`Petfinder` class by :code:`petpy.Petfinder`.

Version 1.7.2
-------------

- There is now a proper message when the daily API call limit is exceeded. Before the change, methods would return a
  :code:`JSONDecodeError`.
- The Python 2 to 3 compatibility package :code:`six`, has been added as a requirement for package installation.
  The :code:`six` library is lightweight and ensures the :code:`petpy` package works properly for Python 2 and 3.
- Numpy is no longer required for installing the package. Numpy's :code:`nan` was initially used to denoted shelters
  and animals that were not found in the Petfinder database. The value returned when a shelter or animal is not found
  is now 'na'.

Version 1.7.1
-------------

- Fix to the :code:`shelter_get()` method for handling empty responses when no shelters returned for when
  the parameter :code:`return_df = True`.
- Fix to getting pets available at a shelter with :code:`shelter_get_pets()` when the parameter
  :code:`return_df = True` when the given shelter does not return any available animals.

Version 1.7.0
-------------

- Refactoring of the library to clean up code files.
- Fixed a bug with the :code:`shelter_get_pets()` method that caused an error to be thrown when there is only
  one pet record and the parameter :code:`return_df = True`.
- Many changes to simplify expressions and internal code within methods.
- The Petfinder class method names and parameters have been renamed to be PEP8 compatible. I apologize as this will
  cause backward compatibility issues upon updating for anyone using previous versions. The original intention of the
  naming was to reflect the Petfinder API's method names as closely as possible, but after further consideration and
  given the relatively short life of the library, I think the change is necessary for the future growth and maturity
  of the package.
- How the methods interact with the Petfinder API is unchanged. Thus there is no immediate need to update your
  version of petpy if it will break any current code.
- The Github repo README has been updated with the new API methods.
- Below is a table detailing the changed method names:

=====================   =======================
Previous Method Name    New Method Name
=====================   =======================
pet_getRandom()         pet_get_random()
shelter_getPets()       shelter_get_pets()
shelter_listByBreed()   shelter_list_by_breed()
=====================   =======================

- The following lists the method parameter names that have changed with the release:

=======================  ==================
Previous Parameter Name  New Parameter Name
=======================  ==================
petId                    pet_id
shelterId                shelter_id
=======================  ==================

Version 1.6.0
-------------

- This release removes pandas as an installation requirement for the package. Although pandas is
  required to convert the API results into a DataFrame, this is optional and not necessary to the
  building or use of the package itself.

Version 1.5.995
---------------

- Calls that return JSON results when using the :code:`pet_find()` method when :code:`return_df=True` are now
  adequately handled and an empty pandas DataFrame is returned. This result can happen when searching for a particular
  breed of animal that is currently not available in the Petfinder database.

Version 1.5.92
--------------

- The paged results should now cap at Petfinder's 2,000 search limit consistently.
- The methods :code:`shelter_get()` and :code:`shelters_get()` now handle shelters that have opted-out of having
  their information available in the Petfinder API.

Version 1.5.91
--------------

- Paged results will now reach Petfinder's 2,000 records per search limit. Before, if the next paged result would
  equal or exceed 2,000 results the call would end, and the results would be returned. For example, if the parameters
  :code:`pages` is 10 and :code:`count` is 200, 2,000 records will now be returned, whereas previously 1,800 would
  be returned.

Version 1.5.9
-------------

- Paging results that exceed Petfinder's limit of 2,000 records returned per search with :code:`return_df = True`
  will now correctly exit the loop and return the results as a DataFrame.

Version 1.5.7
-------------

- The fix to returning a DataFrame when paging results is now implemented in this release. Apologies for the
  oversight, the code change was not made before releasing the previous version.
- The contact information returned with a DataFrame when :code:`return_df = True` now has the prefix 'contact.'
  removed to make the results cleaner.

Version 1.5.6
-------------

- Paging results now returns the stated number of pages in the :code:`pages` parameter. Before, :code:`pages + 1`
  results were returned.
- Returning pandas DataFrames with methods :code:`pet_find()` and :code:`shelter_find()` should no longer throw
  :code:`ValueError` (duplicate column name was causing an error in concatenating the list of results into a DataFrame).

Version 1.5.5
-------------

- :code:`shelter_getPets()` method now returns a complete flattened pandas DataFrame when the parameter
  :code:`return_df = True`.

Version 1.5.4
-------------

- Slight fix to :code:`pet_getRandom()` method. Before, if the method parameter :code:`return_df = True`, but
  the parameter :code:`output` was not one of 'basic' or 'full', the :code:`return_df` parameter was overridden
  and set as :code:`False`. Now, if :code:`return_df = True` and :code:`output` :code:`None`, then
  :code:`output` is set to 'full' to return the most complete DataFrame.
- Added :code:`records` parameter to :code:`pet_getRandom()` to allow multiple random results to be returned in the
  same method call. Please note each record returned counts as one call made to the Petfinder API.
- Added API convenience methods :code:`pets_get()` and :code:`shelters_get()` for pulling multiple results given a
  list or tuple of IDs. These methods are essentially wrappers of the API methods :code:`pet_get()` and
  :code:`shelter_get()`.
- More code cleanup, formatting, and simplification.

Version 1.5.0
-------------

- Add option to convert returned results into a pandas DataFrame.
- Formatting and code cleanup.
- Updated docstrings

Version 1.0.0
-------------

First major release.