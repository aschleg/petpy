
# Version History

Changelog and version changes made with each release.

## Version 2.3.1

* Removed rate check limits that were causing errors with trying to call more
  than one page for several endpoint functions. 

## Version 2.3.0

* Added several additional search filters to the `animals()` function.
    - `declawed`: Filters results by animals that are marked as declawed.
    - `house_trained`: Filters results by animals that are house trained.
    - `special_needs`: Filters results by animals that have special needs
* Search filters that can take multiple values in the `animals()` function, 
  including `age`, `gender`, `status`, `animal_type`, `size`, and `coat`, should 
  now correctly accept both comma-delimited strings, such as `age='baby,'young'` 
  and lists or tuples.
* The required version for `pandas` has been updated to at least version `1.0.0`

## Version 2.2.1

Very small maintenance patch to update several `setup.py` settings. There is no need to update to this version.

## Version 2.2.0

* Support for Python 3.5 has been discontinued. 
* The `animals()` method has been updated to include new parameters provided by Petfinder's `animal` 
  endpoint. This parameters include:
  - `good_with_cats`: Boolean for filtering animals that are designated as good with cats.
  - `good_with_children`: Boolean for filtering animals that are designated as good with children.
  - `good_with_dogs`: Boolean for filtering animals that are designated as good with dogs.
  - `before_date`: Returns results published before the specified time.
  - `after_date`: Returns results published after the specified time.

## Version 2.1.3

* `organization_id` parameter in the `animals` method should now only return animals from specified organization IDs.

## Version 2.1.2 

New release includes a bug fix and some additional changes for checking total usage against the Petfinder API. 

- `animal_type` parameter used in the `animals()` endpoint has been corrected and should be working properly.
- New methods for checking the usage of the supplied API key against the limits defined by the Petfinder API have been 
  implemented to better help warn users when they are approaching their API request limit.
    - If the `max_pages` parameter exceeds 10,000, a warning will be issued to give the user the opportunity to continue 
      or limit their results to 10,000 pages.
    - When the API limits are exceeded, a `RuntimeError` will be issued. 

Thank you to contributor [ma755](https://github.com/ma7555) for submitting the pull request.

## Version 2.1.1

Small update release to fix the `distance` parameter logic when searching for pets using the `animals()` or
`organizations()` methods. Thank you to contributor [ljlevins](https://github.com/ljlevins) for submitting the pull 
request. 

## Version 2.1.0

The `2.1.0` release of `petpy` implements several user-defined exceptions to help users debug any 
errors that may occur. Although the `petpy` library attempts to find any invalid passed parameter values and raise the 
appropriate error before the call to the Petfinder API is made to reduce the number of calls made to the API; however, 
some errors cannot be caught until after the API call is made. This update introduces these custom, user-defined 
exceptions for debugging error responses from the Petfinder API. For more information on the Petfinder API error 
definitions, please see the [Petfinder API documentation](https://www.petfinder.com/developers/v2/docs/#errors).

The following is a list of the new user-defined exceptions.

- `PetfinderInvalidCredentials`
  - Raised when a user enters invalid API key and secret key credentials.
- `PetfinderInsufficientAccess`
  - Raised when a [status code 403](https://httpstatuses.com/403) occurs. This error would typically be 
    raised when the current authentication token to the Petfinder API has expired and requires the connnection 
    to be re-authenticated.
- `PetfinderResourceNotFound`
  - Raised when a [status code 404](https://httpstatuses.com/404) occurs.
- `PetfinderUnexpectedError`
  - Raised when a [status code 500](https://httpstatuses.com/500) occurs.
- `PetfinderInvalidParameters`
  - Raised when a [400 status code](https://httpstatuses.com/400) occurs. The exception will include the invalid 
  parameters detected by the Petfinder API and include those parameters as part of the error output as a JSON object. 
  For more information on this error, please see the 
  [Petfinder API documentation](https://www.petfinder.com/developers/v2/docs/#err-00002).
    - Please note the `petpy` library will attempt to catch any invalid parameters before the API call is made to avoid 
      extraneous issuage of the API, but if an invalid parameter does get through then this error should help provide 
      the necessary information for users to debug any errors related to their chosen parameters.

The following other changes have been made in the `2.1.0` release.

- The `host` and `auth` attributes of the `Petfinder` class are now private (to the extent that Python allows private 
  attributes, denoted with an underscore in front of the attribute).

## Version 2.0.2

Minor bug fix release with following:

- `breeds()` method now correctly returns data when a single animal type is supplied.
- `animals()` method now properly displays the correct error message when the `distance` parameter is 
0 <= distance <= 500.

## Version 2.0.1

- Fixes the `animals()` and `organizations()` method to return all matching search results when the `pages` parameter 
  is set to `None`.
- The resulting JSON (dictionary) from the `breeds()` method when the parameter `return_df=False` will now consistently 
  have `types` as the key. Prior to this change, if the `breeds()` method was called with a single animal type, the 
  resulting key name in the returned object would be named `type`, whereas if more than one animal type is specified 
  the key name would be `types`.
- The `distance` parameter for the `animals()` and `organizations()` parameters will now raise a `ValueError` if it is 
  less than 0.

# Version 2.0.0

New major release coinciding with the release of [v2.0 of the Petfinder API](https://www.petfinder.com/developers/)! 
The legacy version of the Petfinder API, v1.0, will be retired in January 2020, therefore, the `petpy` library has 
been updated almost from the ground up to be compatible as possible with the new version of the Petfinder API! The 
new version of the Petfinder API is a huge improvement over the legacy version, with many changes and additions to 
the design of the API itself. 

Below is a summary of all the changes made in the release of `petpy 2.0`. 
  
- `petpy` now supports the latest release of Python 3.7
- Support for Python 2.7 is discontinued as Python 2.7 will be officially discontinued in January 2020.
- The following methods have been added to `petpy` to make it compatible with v2.0 of the Petfinder API.
    - `animal_types()` is used to getting animal types (or type) available from the Petfinder API. The release 
      of v2.0 of the Petfinder API added several endpoints for accessing animal types in the Petfinder database.
      This method wraps both Petfinder API endpoints for getting animal types. More information on the animal type 
      endpoints in the Petfinder API can be found in its documentation:
        - [Get Animal Types](https://www.petfinder.com/developers/v2/docs/#get-animal-types)
        - [Get Single Animal Type](https://www.petfinder.com/developers/v2/docs/#get-a-single-animal-type)
    - `breeds()` is the new method for getting available animal breeds from the Petfinder database. The API 
      endpoint documentation is available on the Petfinder API documentation page.
        - [Get Animal Breeds](https://www.petfinder.com/developers/v2/docs/#get-animal-breeds)
    - `animals()` is the method for extracting animal data available on the Petfinder API and deprecates the 
      `pets()` related methods. The method wraps both the `animals` and `animal/{id}` endpoints of the Petfinder API. The documentation for these endpoints can be 
      found in the Petfinder API documentation:
        - [Get Animal](https://www.petfinder.com/developers/v2/docs/#get-animal)
        - [Get Animals](https://www.petfinder.com/developers/v2/docs/#get-animals)
    - `organizations()` is now the method for extracting animal welfare organization data available on Petfinder 
      and deprecates previous `shelter()` related methods and endpoints. The `organizations()` method wraps both 
      the Petfinder API `organizations` and `organizations/{id}` endpoints. The Petfinder API documentation for 
      these two endpoints can be found below:
        - [Get Organizations](https://www.petfinder.com/developers/v2/docs/#get-organizations)
        - [Get Organization](https://www.petfinder.com/developers/v2/docs/#get-organization)
- The following methods have been removed as they are no longer valid endpoints with the release of v2.0 of the 
  PetFinder API. 
    - `pet_get_random()`
    - `shelter_list_by_breed()`
    - `shelter_get_pets()`
- General refactoring and code clean-up.
    

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
