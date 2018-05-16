# Petpy Changelog and Version History

## Version 1.8.0

- General refactoring of the `petpy` library to remove unneeded methods from being exposed when importing the 
  library. The best way to import and begin using `petpy` is `from petpy import Petfinder` or, less 
  optimally, `import petpy`, then calling the `Petfinder` class by `petpy.Petfinder`.

## Version 1.7.2

- There is now a proper message when the daily API call limit is exceeded. Prior to the change, methods would
  return a `JSONDecodeError`.
- The Python 2 to 3 compatibility package `six`, has been added as a requirement for package installation.
  The `six` library is lightweight and ensures the `petpy` package works properly for Python 2 and 3.
- Numpy is no longer required for installing the package. Numpy's `nan` was originally used to denoted shelters
  animals that were not found in the Petfinder database. The value returned when a shelter or animal is not found
  is now 'na'.

## Version 1.7.1

- Fix to the `shelter_get()` method for handling empty responses when no shelters returned for when
  the parameter `return_df = True`.
- Fix to getting pets available at a shelter with `shelter_get_pets()` when the parameter
  `return_df = True` when the given shelter does not return any available animals.

## Version 1.7.0

- Refactoring of library to clean up code files.
- Fixed a bug with the `shelter_get_pets()` method that caused an error to be thrown when there is only
  one pet record and the parameter `return_df = True`.
- Many changes to simplify expressions and internal code within methods.
- The `Petfinder` class method names and parameters have been renamed to be PEP8 compatible. I apologize as this
  will cause backward compatibility issues upon updating for anyone using previous versions. The original
  intention of the naming was to reflect the Petfinder API's method names as closely as possible, but after
  further consideration and given the relative short life of the library, I think the change is necessary for the
  future growth and maturity of the package.
- How the methods interact with the Petfinder API is unchanged, thus there is no immediate need to update your
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

## Version 1.6.0

- This release removes pandas as an installation requirement for the package. Although pandas is
  required to convert the API results into a DataFrame, this is optional and not necessary to the
  building or use of the package itself.

## Version 1.5.995

- Calls that return JSON results when using the `pet_find()` method when `return_df=True` are now
  properly handled and an empty pandas DataFrame is returned. This result can happen when searching for a
  particular breed of animal that is currently not available in the Petfinder database.

## Version 1.5.92

- The paged results should now cap at Petfinder's 2,000 search limit consistently.
- The methods `shelter_get()` and `shelters_get()` now handle shelters that have opted-out of having
  their information available in the Petfinder API.

## Version 1.5.91

- Paged results will now reach Petfinder's 2,000 record per search limit. Before, if the next paged result would
  equal or exceed 2,000 results the call would end and the results would be returned. For example, if the parameters
  `pages` is 10 and `count` is 200, 2,000 records will now be returned, whereas previously 1,800 would
  be returned.

## Version 1.5.9

- Paging results that exceed Petfinder's limit of 2,000 records returned per search with `return_df = True`
  will now properly exit the loop and return the results as a DataFrame.

## Version 1.5.7

- The fix to returning a DataFrame when paging results is now implemented in this release. Apologies for the
  oversight, the code change was not made prior to releasing the previous version.
- The contact information returned with a DataFrame when `return_df = True` now has the prefix 'contact.'
  removed to make the results cleaner.

## Version 1.5.6

- Paging results now returns the stated number of pages in the `pages` parameter. Before, `pages + 1`
  results were returned.
- Returning pandas DataFrames with methods `pet_find()` and `shelter_find()` should no longer throw
  `ValueError` (duplicate column name was causing error in concatenating list of results into a DataFrame).

## Version 1.5.5

- `shelter_getPets()` method now returns a complete flattened pandas DataFrame when the parameter
  `return_df = True`.

## Version 1.5.4

- Slight fix to `pet_getRandom()` method. Before, if the method parameter `return_df = True`, but
  the parameter `output` was not one of 'basic' or 'full', the `return_df` parameter was overridden
  and set as `False`. Now, if `return_df = True` and `output` `None`, then
  `output` is set to 'full' to return the most complete DataFrame.
- Added `records` parameter to `pet_getRandom()` to allow multiple random results to be returned in the
  same method call. Please note each record returned counts as one call made to the Petfinder API.
- Added API convenience methods `pets_get()` and `shelters_get()` for pulling multiple results given a
  list or tuple of IDs. These methods are essentially wrappers of the API methods `pet_get()` and
  `shelter_get()`.
- More code cleanup, formatting and simplification.

## Version 1.5.0

- Add option to convert returned results into a pandas DataFrame.
- Formatting and code cleanup.
- Updated docstrings

## Version 1.0.0

First major release.