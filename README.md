# Petpy - Python Wrapper for the Petfinder API

[![Documentation Status](https://readthedocs.org/projects/petpy/badge/?version=latest)](http://petpy.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/aschleg/petpy.svg?branch=master)](https://travis-ci.org/aschleg/petpy)
[![Build status](https://ci.appveyor.com/api/projects/status/xjxufxt7obd84ygr?svg=true)](https://ci.appveyor.com/project/aschleg/petpy)
[![Coverage Status](https://coveralls.io/repos/github/aschleg/petpy/badge.svg?branch=master)](https://coveralls.io/github/aschleg/petpy?branch=master)

Petpy is an easy-to-use and convenient Python wrapper for the [Petfinder API](https://www.petfinder.com/developers/api-docs).

## Example

After receiving an API key from [Petfinder](https://www.petfinder.com/developers/api-key), usage of petpy to extract
data from the Petfinder database is straightforward.

~~~
import petpy

pf = petpy.Petfinder(key)

cats = pf.breed_list('cat')

pf.pet_getRandom()
~~~

The above simple example creates an authenticated connection to the Petfinder API and then uses that connection to
pull the entire list of cat breeds listed in the Petfinder database. The next line returns a randomly selected
pet record.

## Available Methods

Below is a summary table of the available methods in the petpy library and the accompanying Petfinder API method, as
well as a brief description. Please see the petpy documentation for more information on each method. The Petfinder
API methods documentation can also be found [here](https://www.petfinder.com/developers/api-docs#methods).

| Method                | Petfinder API Method | Description                                                                                        |
|-----------------------|----------------------|----------------------------------------------------------------------------------------------------|
| breed_list()          | breed.list           | Returns the available breeds for the selected animal.                                              |
| pet_find()            | pet.find             | Returns a collection of pet records matching input parameters.                                     |
| pet_get()             | pet.get              | Returns a single record for a pet.                                                                 |
| pet_getRandom()       | pet.getRandom        | Returns a randomly selected pet record. The possible result can be filtered with input parameters. |
| shelter_find()        | shelter.find         | Returns a collection of shelter records matching input parameters.                                 |
| shelter_get()         | shelter.get          | Returns a single shelter record.                                                                   |
| shelter_getPets()     | shelter.getPets      | Returns a collection of pet records for an individual shelter.                                     |
| shelter_listByBreed() | shelter.listByBreed  | Returns a list of shelter IDs listing animals matching the input animal breed.                     |

## Documentation

* [Petpy documentation](http://petpy.readthedocs.io/en/latest/)
* [Petfinder API documentation](https://www.petfinder.com/developers/api-docs)

## Vignettes

A series of IPython notebooks that introduce and explore the `petpy` library.

* [01 - Introduction](docs/vignettes/01-Introduction.ipynb)

## Installation

Petpy is easily installed through `pip`.

~~~~
pip install petpy
~~~~

## Requirements

Python 2.7 or Python >= 3.3

## License

MIT