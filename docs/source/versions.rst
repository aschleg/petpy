.. _versions:

Version History
===============

Changelog and version changes made with each release.

Version 1.5.1
=============

- Slight fix to :code:`pet_getRandom()` method. Before, if the method parameter :code:`return_df = True`, but
  the parameter :code:`output` was not one of 'basic' or 'full', the :code:`return_df` parameter was overridden
  and set as :code:`False`. Now, if :code:`return_df = True` and :code:`output` :code:`None`, then
  :code:`output` is set to 'full' to return the most complete DataFrame.
- More code cleanup, formatting and simplification.
- Add :code:`records` parameter to :code:`pet_getRandom()` to allow multiple random results to be returned in the
  same method call. Please note each record returned counts as one call made to the Petfinder API.

Version 1.5.0
=============

- Add option to convert returned results into a pandas DataFrame.
- Formatting and code cleanup.
- Updated docstrings


Version 1.0.0
=============

First major release.