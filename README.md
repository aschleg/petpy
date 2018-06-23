# Petpy - Python Wrapper for the Petfinder API

[![Documentation Status](https://readthedocs.org/projects/petpy/badge/?version=latest)](http://petpy.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/aschleg/petpy.svg?branch=master)](https://travis-ci.org/aschleg/petpy)
[![Build status](https://ci.appveyor.com/api/projects/status/xjxufxt7obd84ygr?svg=true)](https://ci.appveyor.com/project/aschleg/petpy)
[![Coverage Status](https://coveralls.io/repos/github/aschleg/petpy/badge.svg?branch=master)](https://coveralls.io/github/aschleg/petpy?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ac2a4c228a9e425ba11af69f7a5c9e51)](https://www.codacy.com/app/aschleg/petpy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=aschleg/petpy&amp;utm_campaign=Badge_Grade)
![https://pypi.org/project/petpy/](https://img.shields.io/badge/pypi%20version-1.8.0-blue.svg)
![https://pypi.org/project/petpy/](https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg)

:cat2: :dog2: :rooster: :rabbit2: :racehorse:

Petpy is an easy-to-use and convenient Python wrapper for the [Petfinder API](https://www.petfinder.com/developers/api-docs).

## Installation

`petpy` is easily installed through `pip`.

~~~ python
pip install petpy
~~~

The library can also be cloned or downloaded into a location of your choosing and then installed using the `setup.py` 
file per the following:

~~~ python
git clone git@github.com:aschleg/petpy.git
cd petpy
python setup.py install
~~~

## Examples and Usage

After receiving an API key from [Petfinder](https://www.petfinder.com/developers/api-key), usage of `petpy` to extract
data from the Petfinder database is straightforward.

### Authenticating with the Petfinder API

Authenticating the connection with the Petfinder API is as simple as initializing the `Petfinder` class with an API 
key received from Petfinder.

~~~ python
pf = Petfinder(key)
~~~

### Getting currently listed animal breeds on Petfinder

Once the `Petfinder` class has been initialized with a key received from Petfinder, the methods can then be used to 
interact with and extract data from the Petfinder API. In this example, we use the `pf` object created above to get 
the currently listed breeds of cats and dogs.

~~~ python
cat_breeds = pf.breed_list('cat')
dog_breeds = pf.breed_list('dog')

# The method can also be set to coerce the returned JSON results into a pandas DataFrame by setting the parameter 
return_df = True.

cat_breeds_df = pf.breed_list('cat', return_df = True)
dog_breeds_df = pf.breed_list('dog', return_df = True)
~~~

### Finding available pets in specific locations

The `pet_find` method returns animals available on Petfinder at local animal shelters given a specific location. The 
location can be as granular as a city or as broad as a country in North America. For example, let's say we are 
interested in finding the first 100 female cats available for adoption in the Seattle area and coerce the default 
JSON results into a pandas DataFrame for easier analysis.

~~~ python
wa_female_cats = pf.pet_find(location='Seattle', 
                             animal='cat', 
                             sex='Female', 
                             count=100, 
                             return_df=True) 
~~~

### Locating animal shelters in a given location

The `shelter_find` method is similar to the `pet_find` method above, with the exception that it returns the location 
and information on shelters within the given region specified in the `location` parameter. The Petfinder API will 
automatically extend its search for shelters if the `count` exceeds the number of shelters in the specified area. For 
example, let's say we wanted to find 500 animal shelters in Seattle, Washington. As there are not 500 shelters in 
Seattle alone, the API will expand its return results to include likely most, if not, all of Washington State and 
likely surrounding states like Oregon and Idaho until it finds 500 shelters to return. As with the `pet_find` method, 
the `shelter_find` method also has a `return_df` parameter that automatically transforms the returned JSON data from 
the API into a pandas DataFrame. 

~~~ python
wa_shelters = pf.shelter_find(location='Seattle',
                              count=500,
                              return_df=True)
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

## Introduction and Example Uses of `petpy`

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/aschleg/petpy/master?filepath=notebooks)

A series of IPython notebooks that introduce and explore some of the functionality and possible uses of the 
`petpy` library. The notebooks can also be launched interactively with [binder](https://mybinder.org/) by clicking the 
"launch binder" badge.

* [01 -Introduction to petpy](https://github.com/aschleg/petpy/blob/master/notebooks/01-Introduction%20to%20petpy.ipynb)
* [02 - Download 45,000 Adoptable Cat Images using petpy and multiprocessing](https://github.com/aschleg/petpy/blob/master/notebooks/02-Download%2045%2C000%20Adoptable%20Cat%20Images%20with%20petpy%20and%20multiprocessing.ipynb)

## Documentation

* [Petpy documentation](http://petpy.readthedocs.io/en/latest/)
* [Petpy changelog](https://github.com/aschleg/petpy/blob/master/CHANGELOG.md)
* [Petfinder API documentation](https://www.petfinder.com/developers/api-docs)

## Requirements

* Python 2.7 or Python >= 3.4
* [requests](http://docs.python-requests.org/en/master/) >= 2.18.4
* Although not strictly required for installation or use, the [pandas](https://pandas.pydata.org/) library is needed 
for returning the results as a DataFrame.

## License

MIT