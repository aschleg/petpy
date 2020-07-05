[![Documentation Status](https://readthedocs.org/projects/petpy/badge/?version=latest)](http://petpy.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/aschleg/petpy.svg?branch=master)](https://travis-ci.org/aschleg/petpy)
[![Coverage Status](https://coveralls.io/repos/github/aschleg/petpy/badge.svg?branch=master)](https://coveralls.io/github/aschleg/petpy?branch=master)
[![codecov](https://codecov.io/gh/aschleg/petpy/branch/master/graph/badge.svg)](https://codecov.io/gh/aschleg/petpy)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ac2a4c228a9e425ba11af69f7a5c9e51)](https://www.codacy.com/app/aschleg/petpy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=aschleg/petpy&amp;utm_campaign=Badge_Grade)
[![Dependencies](https://img.shields.io/librariesio/github/aschleg/petpy.svg?label=dependencies)](https://libraries.io/github/aschleg/petpy)
[![https://pypi.org/project/petpy/](https://img.shields.io/badge/pypi%20version-2.2.0-blue.svg)](https://pypi.org/project/petpy/)
[![https://pypi.org/project/petpy/](https://img.shields.io/badge/python-3.6%2C%203.7-blue.svg)](https://pypi.org/project/petpy/)

:cat2: :dog2: :rooster: :rabbit2: :racehorse:

### Installation

`petpy` is easily installed through `pip`.

~~~ python
pip install petpy
~~~

`petpy` can also be cloned or downloaded into a location of your choosing and then installed using the `setup.py` 
file per the following:

~~~ python
git clone git@github.com:aschleg/petpy.git
cd petpy
python setup.py install
~~~

### Authenticating with the Petfinder API

Authenticating the connection with the Petfinder API is done at the same time the `Petfinder` class is initialized. An 
account must first be created with [Petfinder](https://www.petfinder.com/developers/) to receive an API and secret 
key. The API and Secret key will be used to grant access to the Petfinder API, which lasts for 3600 seconds, or one 
hour. After the authentication period ends, you must re-authenticate with the Petfinder API.

### Requirements

* Python >= 3.6
* [requests](http://docs.python-requests.org/en/master/) >= 2.18.4
* Although not strictly required to use `petpy`, the [pandas](https://pandas.pydata.org/) library is needed 
  for returning the results as a DataFrame.
  
### About [Petfinder.com](https://www.petfinder.com)

Petfinder.com is one of the largest online, searchable databases for finding a new pet online. The database contains 
information on over 14,000 animal shelters and adoption organizations across North America with nearly 300,000 animals 
available for adoption. Not only does this make it a great resource for those looking to adopt their new best friend, 
but the data and information provided in Petfinder's database makes it ideal for analysis. 