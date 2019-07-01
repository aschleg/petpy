# Version 2.0.0

New major release coninciding with the release of [v2.0 of the Petfinder API](https://www.petfinder.com/developers/)! 
The legacy version of the Petfinder API, v1.0, will be retired in January 2020, therefore, the `petpy` library has 
been updated almost from the ground up to be compatible as possible with the new version of the Petfinder API! The 
new version of the Petfinder API is a huge improvement over the legacy version, with many changes and additions to 
the design of the API itself. As such, several methods from earlier releases of `petpy` that wrapped these endpoints 
will be deprecated over the next few releases.

Below is a summary of all the changes made in the release of `petpy 2.0`. 
  
- Changes Made
    - `petpy` now supports the latest release of Python 3.7
    - Added method `get_animal_types` for getting animal types (or type) available from the Petfinder API. The release 
      of v2.0 of the Petfinder API added several endpoints for accessing animal types in the Petfinder database. 
      More information on the animal type endpoints in the Petfinder API can be found in its documentation:
        - [Get Animal Types](https://www.petfinder.com/developers/v2/docs/#get-animal-types)
        - [Get Single Animal Type](https://www.petfinder.com/developers/v2/docs/#get-a-single-animal-type)
    - New method for getting available animal breeds from the Petfinder database, `breeds` has been added. This new 
      method depreciates `breed_list` which was based on the Petfinder API v1.0. The API endpoint documentation is 
      available on the Petfinder API documentation page.
        - [Get Animal Breeds](https://www.petfinder.com/developers/v2/docs/#get-animal-breeds)

## Version 1.8.2

- Add `pandas` back as an installation requirement as it is included in top-level imports. `pandas` is 
  still not necessary to use the primary functionality of `petpy`.

## Version 1.8.1

- Implement check to make sure `count` parameter is not larger than 1,000 records (per the Petfinder API
  limits). If `count` exceeds 1,000 a `ValueError` is raised.
- Add check for ensuring the number of total records to return does not exceed 2,000 when paging results with
  the `pages` and `count` parameters. If the desired amount of records is higher than 2,000, a
  `ValueError` is raised.
- Remove Python 3.3 support. Although `petpy` should work fine for those still using Python 3.3, testing for 3.3
  has been discontinued.

## Version 1.8.0

- General refactoring of the `petpy` library to remove unneeded methods from being exposed when importing the 
  library. The best way to import and begin using `petpy` is `from petpy import Petfinder` or, less optimally, 
  `import petpy`, then calling the `Petfinder` class by `petpy.Petfinder`.

## Version 1.7.2

- There is now a proper message when the daily API call limit is exceeded. Before the change, methods would
  return a `JSONDecodeError`.
- The Python 2 to 3 compatibility package `six`, has been added as a requirement for package installation.
  The `six` library is lightweight and ensures the `petpy` package works properly for Python 2 and 3.
- Numpy is no longer required for installing the package. Numpy's `nan` was initially used to denoted shelters animals 
  that were not found in the Petfinder database. The value returned when a shelter or animal is not found is now 'na'.

## Version 1.7.1

- Fix to the `shelter_get()` method for handling empty responses when no shelters returned for when
  the parameter `return_df = True`.
- Fix to getting pets available at a shelter with `shelter_get_pets()` when the parameter
  `return_df = True` when the given shelter does not return any available animals.

## Version 1.7.0

- Refactoring of the library to clean up code files.
- Fixed a bug with the `shelter_get_pets()` method that caused an error to be thrown when there is only
  one pet record and the parameter `return_df = True`.
- Many changes to simplify expressions and internal code within methods.
- The `Petfinder` class method names and parameters have been renamed to be PEP8 compatible. I apologize as this will 
  cause backward compatibility issues upon updating for anyone using previous versions. The original intention of the 
  naming was to reflect the Petfinder API's method names as closely as possible, but after further consideration and 
  given the relatively short life of the library, I think the change is necessary for the future growth and maturity 
  of the package.
- How the methods interact with the Petfinder API is unchanged. Thus there is no immediate need to update your
  version of petpy if it will break any current code.
- The Github repo README has been updated with the new API methods.
- Below is a table detailing the changed method names:

| Previous Method Name | New Method Name |
| -------------------------- | ---------------------- |
| pet_getRandom()           | pet_get_random()     |
| shelter_getPets()            | shelter_get_pets()      |
| shelter_listByBreed()      | shelter_list_by_breed() |

- The following lists the method parameter names that have changed with the release:

| Previous Parameter Name | New Parameter Name |
| ---------------------------- | ------------------------- |
| petId                                 | pet_id                            |
| shelterId                           | shelter_id                       |

## Version 1.6.0

- This release removes pandas as an installation requirement for the package. Although pandas is
  required to convert the API results into a DataFrame, this is optional and not necessary to the
  building or use of the package itself.

## Version 1.5.995

- Calls that return JSON results when using the `pet_find()` method when `return_df=True` are now
  adequately handled and an empty pandas DataFrame is returned. This result can happen when searching for a
  particular breed of animal that is currently not available in the Petfinder database.

## Version 1.5.92

- The paged results should now cap at Petfinder's 2,000 search limit consistently.
- The methods `shelter_get()` and `shelters_get()` now handle shelters that have opted-out of having
  their information available in the Petfinder API.

## Version 1.5.91

- Paged results will now reach Petfinder's 2,000 records per search limit. Before, if the next paged result would 
  equal or exceed 2,000 results the call would end, and the results would be returned. For example, if the parameters 
  `pages` is 10 and `count` is 200, 2,000 records will now be returned, whereas previously 1,800 would be returned.

## Version 1.5.9

- Paging results that exceed Petfinder's limit of 2,000 records returned per search with `return_df = True`
  will now correctly exit the loop and return the results as a DataFrame.

## Version 1.5.7

- The fix to returning a DataFrame when paging results is now implemented in this release. Apologies for the
  oversight, the code change was not made before releasing the previous version.
- The contact information returned with a DataFrame when `return_df = True` now has the prefix 'contact.'
  removed to make the results cleaner.

## Version 1.5.6

- Paging results now returns the stated number of pages in the `pages` parameter. Before, `pages + 1`
  results were returned.
- Returning pandas DataFrames with methods `pet_find()` and `shelter_find()` should no longer throw
  `ValueError` (duplicate column name was causing an error in concatenating a list of results into a DataFrame).

## Version 1.5.5

- `shelter_getPets()` method now returns a complete flattened pandas DataFrame when the parameter
  `return_df = True`.

## Version 1.5.4

- Slight fix to `pet_getRandom()` method. Before, if the method parameter `return_df = True`, but the parameter `output` 
  was not one of 'basic' or 'full', the `return_df` parameter was overridden and set as `False`. Now, if 
  `return_df = True` and `output` `None`, then `output` is set to 'full' to return the complete DataFrame.
- Added `records` parameter to `pet_getRandom()` to allow multiple random results to be returned in the same method 
  call. Please note each record returned counts as one call made to the Petfinder API.
- Added API convenience methods `pets_get()` and `shelters_get()` for pulling multiple results given a list or tuple 
  of IDs. These methods are essentially wrappers of the API methods `pet_get()` and `shelter_get()`.
- More code cleanup, formatting, and simplification.

## Version 1.5.0

- Add option to convert returned results into a pandas DataFrame.
- Formatting and code cleanup.
- Updated docstrings

# Version 1.0.0

First major release.