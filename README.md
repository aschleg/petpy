# Petpy - Python Wrapper for the Petfinder API

[![Documentation Status](https://readthedocs.org/projects/petpy/badge/?version=latest)](http://petpy.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/aschleg/petpy.svg?branch=master)](https://travis-ci.org/aschleg/petpy)
[![Build status](https://ci.appveyor.com/api/projects/status/xjxufxt7obd84ygr?svg=true)](https://ci.appveyor.com/project/aschleg/petpy)
[![Coverage Status](https://coveralls.io/repos/github/aschleg/petpy/badge.svg?branch=master)](https://coveralls.io/github/aschleg/petpy?branch=master)
[![Code Health](https://landscape.io/github/aschleg/petpy/master/landscape.svg?style=flat)](https://landscape.io/github/aschleg/petpy/master)

Petpy is an easy-to-use and convenient Python wrapper for the [Petfinder API](https://www.petfinder.com/developers/api-docs).

## Example

After receiving an API key from [Petfinder](https://www.petfinder.com/developers/api-key), usage of petpy to extract
data from the Petfinder database is straightforward.

~~~
import petpy

pf = petpy.Petfinder(key) # create connection to Petfinder API

cats = pf.breed_list('cat') # return all the listed cats breeds on the Petfinder website in JSON format

# The following returns the first 1,000 cat records in Washington in the Petfinder database as a pandas DataFrame.
cats_wa = pf.pet_find(location='WA', animal='cat', count=1000, return_df=True)

pf.pet_getRandom() # return a random pet record
~~~

## Available Methods

Below is a summary table of the available methods in the petpy library and the accompanying Petfinder API method, as
well as a brief description. Please see the petpy documentation for more information on each method. The Petfinder
API methods documentation can also be found [here](https://www.petfinder.com/developers/api-docs#methods). All 
functions have a `return_df` parameter that when set to `True`, returns a pandas DataFrame of the results to facilitate 
more efficient data analysis.

| Method                  | Petfinder API Method | Description                                                                                        |
|-------------------------|----------------------|----------------------------------------------------------------------------------------------------|
| breed_list()            | breed.list           | Returns the available breeds for the selected animal.                                              |
| pet_find()              | pet.find             | Returns a collection of pet records matching input parameters.                                     |
| pet_get()               | pet.get              | Returns a single record for a pet.                                                                 |
| pet_get_random()        | pet.getRandom        | Returns a randomly selected pet record. The possible result can be filtered with input parameters. |
| shelter_find()          | shelter.find         | Returns a collection of shelter records matching input parameters.                                 |
| shelter_get()           | shelter.get          | Returns a single shelter record.                                                                   |
| shelter_get_pets()      | shelter.getPets      | Returns a collection of pet records for an individual shelter.                                     |
| shelter_list_by_breed() | shelter.listByBreed  | Returns a list of shelter IDs listing animals matching the input animal breed.                     |

## Documentation

* [Petpy documentation](http://petpy.readthedocs.io/en/latest/)
* [Petfinder API documentation](https://www.petfinder.com/developers/api-docs)

## Vignettes and Introduction to petpy

[![Binder](https://mybinder.org/badge.svg)](https://hub.mybinder.org/user/aschleg-petpy-klvuc0pp/tree/docs/notebooks)

A series of IPython notebooks that introduce and explore some of the functionality and possible uses of the 
`petpy` library. The notebooks can also be launched interactively with [binder](https://mybinder.org/) by clicking the 
"launch binder" badge.

* [01 -Introduction to petpy](https://github.com/aschleg/petpy/blob/master/docs/notebooks/01-Introduction%20to%20petpy.ipynb)
* [02 - Download 45,000 Adoptable Cat Images using petpy and multiprocessing](https://github.com/aschleg/petpy/blob/master/docs/notebooks/02-Download%2045%2C000%20Adoptable%20Cat%20Images%20with%20petpy%20and%20multiprocessing.ipynb)

## Installation

Petpy is easily installed through `pip`.

~~~~
pip install petpy
~~~~

## Requirements

* Python 2.7 or Python >= 3.3
* [requests](http://docs.python-requests.org/en/master/) >= 2.18.4
* Although not strictly required for installation, the [pandas](https://pandas.pydata.org/) library is needed for 
returning the results as a DataFrame.

## License

MIT