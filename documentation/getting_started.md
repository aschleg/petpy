layout: page
title: 'Getting Started'
permalink: documentation/getting-started/

# Getting Started

This is a quick introduction to how to get started with the `petpy` library. If not done already, install `petpy` using 
`pip`.

~~~ python
pip install petpy
~~~

Or, if preferred, the most recent development version of `petpy` can be installed by downloading the library from 
Github.

~~~ python
git clone git@github.com:aschleg/petpy.git
cd petpy
python setup.py install
~~~

After installing `petpy`, the next step is to receive an API and Secret key from Petfinder.com

# Creating a Petfinder.com Developer Account

An account must first be created with [Petfinder](https://www.petfinder.com/developers/) to receive an API and secret 
key. These keys will be used to authenticate and grant access to the Petfinder API through 
[OAuth2](https://oauth.net/2/). After receiving the API and Secret key from Petfinder, you are ready to start using the 
`petpy` library.

# Authenticating to the Petfinder.com API

Authenticating the connection with the Petfinder API is done at the same time the `Petfinder` class is initialized. 

~~~ python
from petpy import Petfinder
pf = Petfinder(key=API_KEY, 
               secret=SECRET_KEY)
~~~

You are now ready to start using `petpy` to get data from Petfinder.com's API! The following are some examples on using 
the `petpy` library.

## Finding animal types

~~~ python
# All animal types and their relevant data.
all_types = pf.animal_types()

# Returning data for a single animal type
dogs = pf.animal_types('dog')

# Getting multiple animal types at once
cat_dog_rabbit_types = pf.animal_types(['cat', 'dog', 'rabbit'])
~~~

## Getting animal breeds for available animal types

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

## Finding available animals on Petfinder

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

## Getting animal welfare organizations in the Petfinder database 

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
