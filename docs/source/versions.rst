.. _versions:

Version History
===============

Changelog and version changes made with each release.

Version 1.5.91
--------------

- Paged results will now reach Petfinder's 2,000 record per search limit. Before, if the next paged result would
  equal or exceed 2,000 results the call would end and the results would be returned. For example, if the parameters
  :code:`pages` is 10 and :code:`count` is 200, 2,000 records will now be returned, whereas previously 1,800 would
  be returned.

Version 1.5.9
-------------

- Paging results that exceed Petfinder's limit of 2,000 records returned per search with :code:`return_df = True`
  will now properly exit the loop and return the results as a DataFrame.

Version 1.5.7
-------------

- The fix to returning a DataFrame when paging results is now implemented in this release. Apologies for the
  oversight, the code change was not made prior to releasing the previous version.
- The contact information returned with a DataFrame when :code:`return_df = True` now has the prefix 'contact.'
  removed to make the results cleaner.

Version 1.5.6
-------------

- Paging results now returns the stated number of pages in the :code:`pages` parameter. Before, :code:`pages + 1`
  results were returned.
- Returning pandas DataFrames with methods :code:`pet_find()` and :code:`shelter_find()` should no longer throw
  :code:`ValueError` (duplicate column name was causing error in concatenating list of results into a DataFrame).

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
- More code cleanup, formatting and simplification.

Version 1.5.0
-------------

- Add option to convert returned results into a pandas DataFrame.
- Formatting and code cleanup.
- Updated docstrings

Version 1.0.0
-------------

First major release.