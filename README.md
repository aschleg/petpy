# Petpy - Python Wrapper for the Petfinder API

[![Documentation Status](https://readthedocs.org/projects/petpy/badge/?version=latest)](http://petpy.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/aschleg/petpy/badge.svg?branch=master)](https://coveralls.io/github/aschleg/petpy?branch=master)
[![codecov](https://codecov.io/gh/aschleg/petpy/branch/master/graph/badge.svg)](https://codecov.io/gh/aschleg/petpy)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ac2a4c228a9e425ba11af69f7a5c9e51)](https://www.codacy.com/app/aschleg/petpy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=aschleg/petpy&amp;utm_campaign=Badge_Grade)
[![Dependencies](https://img.shields.io/librariesio/github/aschleg/petpy.svg?label=dependencies)](https://libraries.io/github/aschleg/petpy)
[![https://pypi.org/project/petpy/](https://img.shields.io/badge/pypi%20version-2.3.1-blue.svg)](https://pypi.org/project/petpy/)
[![https://pypi.org/project/petpy/](https://img.shields.io/badge/python-3.6%2C%203.7%2C%203.8-blue.svg)](https://pypi.org/project/petpy/)

:cat2: :dog2: :rooster: :rabbit2: :racehorse:

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

## Examples and usage

An account must first be created with [Petfinder](https://www.petfinder.com/developers/) to receive an API and secret 
key. The API and secret key will be used to grant access to the Petfinder API, which lasts for 3600 seconds, or one 
hour. After the authentication period ends, you must re-authenticate with the Petfinder API. The following are some 
quick examples for using `petpy` to get started. More in-depth tutorials for `petpy` and some examples of what 
can be done with the library, please see the More Examples and Tutorials section below.

### Authenticating with the Petfinder API

Authenticating the connection with the Petfinder API is done at the same time the `Petfinder` class is initialized.

~~~ python
pf = Petfinder(key=key, secret=secret)
~~~

The following are some quick examples for getting started with `petpy` and the Petfinder API.
### Finding animal types

~~~ python
# All animal types and their relevant data.
all_types = pf.animal_types()

# Returning data for a single animal type
dogs = pf.animal_types('dog')

# Getting multiple animal types at once
cat_dog_rabbit_types = pf.animal_types(['cat', 'dog', 'rabbit'])
~~~

### Getting animal breeds for available animal types

~~~ python
cat_breeds = pf.breeds('cat')
dog_breeds = pf.breeds('dog')

# All available breeds or multiple breeds can also be returned.

all_breeds = pf.breeds()
cat_dog_rabbit = pf.breeds(types=['cat', 'dog', 'rabbit'])
~~~ 

The `breeds` method can also be set to coerce the returned JSON results into a pandas DataFrame by setting 
the parameter `return_df = True`.

~~~ python
cat_breeds_df = pf.breeds('cat', return_df = True)
all_breeds_df = pf.breeds(return_df = True)
~~~

### Finding available animals on Petfinder

The `animals()` method returns animals based on specified criteria that are listed in the Petfinder database. Specific 
animals can be searched using the `animal_id` parameter, or a search of the database can be performed by entering 
the desired search criteria.

~~~ python
# Getting first 20 results without any search criteria
animals = pf.animals()

# Extracting data on specific animals with animal_ids

animal_ids = []
for i in animals['animals'][0:3]:
    animal_ids.append(i['id'])
    
animal_data = pf.animals(animal_id=animal_ids)

# Returning a pandas DataFrame of the first 150 animal results
animals = pf.animals(results_per_page=50, pages=3, return_df=True)
~~~

### Getting animal welfare organizations in the Petfinder database 

Similar to the `animals()` method described above, the `organizations()` method returns data on animal welfare 
organizations listed in the Petfinder database based on specific criteria, if any. In addition to a general search 
of animal welfare organizations, specific organizational data can be extracted by supplying the `organizations()` 
method with organization IDs.

~~~ python
# Return the first 1,000 animal welfare organizations as a pandas DataFrame

organizations = pf.organizations(results_per_page=100, pages=10, return_df=True)

# Get organizations in the state of Washington

wa_organizations = pf.organizations(state='WA')
~~~

## More Examples and Tutorials

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/aschleg/petpy/master?filepath=notebooks)

A series of IPython notebooks that introduce and explore some of the functionality and possible uses of the 
`petpy` library. The notebooks can also be launched interactively with [binder](https://mybinder.org/) by clicking the 
"launch binder" badge.

* [01 -Introduction to petpy](https://github.com/aschleg/petpy/blob/master/notebooks/01-Introduction%20to%20petpy.ipynb)
* [02 - Download 45,000 Adoptable Cat Images using petpy and multiprocessing](https://github.com/aschleg/petpy/blob/master/notebooks/02-Download%2045%2C000%20Adoptable%20Cat%20Images%20with%20petpy%20and%20multiprocessing.ipynb)
  - Please note the following notebook is still based on the legacy version of Petfinder and thus are not fully 
    representative of the functionality and methods of the most recent version of `petpy` and the Petfinder API. These 
    are currently being updated to reflect the new version of `petpy`.
* [03 - Download Pure Breeds Cat Images with petpy for Deep Neural Network training](https://github.com/aschleg/petpy/blob/master/notebooks/03-Download%20Pure%20Breeds%20Cat%20Images%20with%20petpy%20for%20Deep%20Neural%20Network%20training%20-%20multiprocessing.ipynb)
  - Provided by contributor [ma755](https://github.com/ma7555)

### Other

The following are longer usage examples and tutorials that have been posted to external media websites such as 
[Medium.com](medium.com):

* [Analyze Petfinder Adoptable Pet Descriptions with the IBM Watson Tone Analyzer — Part One](https://medium.com/@AaronSchlegel/analyze-petfinder-adoptable-pet-descriptions-with-the-ibm-watson-tone-analyzer-part-one-4efabaa1164b)

## Documentation

* [Petpy documentation](http://petpy.readthedocs.io/en/latest/)
* [Petpy changelog](https://github.com/aschleg/petpy/blob/master/CHANGELOG.md)
* [Petfinder API v2.0 documentation](https://www.petfinder.com/developers/v2/docs/)

## Requirements

* Python >= 3.6
* [requests](http://docs.python-requests.org/en/master/) >= 2.18.4
* Although not strictly required to use `petpy`, the [pandas](https://pandas.pydata.org/) library is needed 
  for returning the results as a DataFrame.

## About [Petfinder.com](https://www.petfinder.com)

Petfinder.com is one of the largest online, searchable databases for finding a new pet online. The database contains 
information on over 14,000 animal shelters and adoption organizations across North America with nearly 300,000 animals 
available for adoption. Not only does this make it a great resource for those looking to adopt their new best friend, 
but the data and information provided in Petfinder's database makes it ideal for analysis. 

## Contributors

* [ma755](https://github.com/ma7555) - Fixed several functions that use an `animal` parameter and 
  implementing checks for exceeding the Petfinder API limit.
* [ljlevins](https://github.com/ljlevins) - Found and fixed an error with the `distance` parameter used in the 
  `organizations` API endpoint.  

## License

MIT
