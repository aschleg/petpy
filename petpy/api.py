# encoding=utf-8

r"""

The :code:`api.py` file stores all the :code:`Petfinder` class and all associated functions and methods for
interacting with the Petfinder API. Before getting started with :code:`petpy`, please be sure to obtain an
API and secret key from Petfinder by registering for an account on the Petfinder developers page at
https://www.petfinder.com/developers/

"""


import datetime
from urllib.parse import urljoin

import pandas as pd
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
from pandas import json_normalize
import requests

from petpy.petpy_types import (
    AnimalTypes,
    AnimalFeatures,
    Animals,
    Date,
    PetfinderID
)
from petpy.exceptions import (
    PetfinderInvalidCredentials,
    PetfinderInsufficientAccess,
    PetfinderResourceNotFound,
    PetfinderUnexpectedError,
    PetfinderInvalidParameters,
    PetfinderRateLimitExceeded
)

#################################################################################################################
#
# Petfinder Class
#
#################################################################################################################


class Petfinder(object):
    r"""
    Wrapper class for the PetFinder API.

    Attributes
    ----------
    key : str
        The key from the Petfinder API passed when the :code:`Petfinder` class is initialized.
    secret : str
        The secret key obtained from the Petfinder API passed when the :code:`Petfinder` class is initialized.

    Methods
    -------
    animal_types(types, return_df=False)
        Returns data on an animal type, or types, available from the Petfinder API.
    breeds(types=None, return_df=False, raw_results=False)
        Returns available breeds of specified animal type(s) from the Petfinder API.
    animals(animal_id=None, animal_type=None, breed=None, size=None, gender=None, age=None, color=None,
            coat=None, status=None, name=None, organization_id=None, location=None, distance=None,
            sort=None, pages=None, results_per_page=20, return_df=False)
        Finds adoptable animals based on given criteria.
    organizations(organization_id=None, name=None, location=None, distance=None, state=None, country=None,
                  query=None, sort=None, results_per_page=20, pages=None, return_df=False)
        Finds animal organizations based on specified criteria in the Petfinder API database.

    """
    def __init__(self, key: str, secret: str):
        r"""
        Initialization method of the :code:`Petfinder` class.

        Parameters
        ----------
        key : str
            API key given after `registering on the PetFinder site <https://www.petfinder.com/developers/api-key>`_
        secret : str
            Secret API key given in addition to general API key. The secret key is required as of V2 of
            the PetFinder API and is obtained from the Petfinder website at the same time as the access key.

        """
        self.key = key
        self.secret = secret
        self._host = 'https://api.petfinder.com/v2/'
        self._access_token = self._authenticate()

    def _authenticate(self) -> str:
        r"""
        Internal function for authenticating users to the Petfinder API.

        Raises
        ------
        PetfinderInvalidCredentials
            Raised if the supplied secret key and secret access key are invalid. Check the generated API key from
            petfinder.com is still active and that the secret and access keys are the same as those passed.

        Returns
        -------
        str
            Access token granted by the Petfinder API. The access token stays live for 3600 seconds, or one hour,
            at which point the user must reauthenticate.

        See Also
        --------
        PetfinderInvalidCredentials

        """
        endpoint = 'oauth2/token'

        url = urljoin(self._host, endpoint)

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.key,
            'client_secret': self.secret
        }
        try:
            r = requests.post(url, data=data)
            return r.json()['access_token']
        except PetfinderUnexpectedError:
            try_count = 1
            while try_count <= 3:
                print(f'Petfinder API encountered an unexpected error during authentication. '
                      f'Re-trying 3 times. Attempt {try_count}')
                self._authenticate()
                try_count += 1
            raise PetfinderUnexpectedError(message="Couldn't authenticate after three tries.",
                                           err=("Petfinder API encountered an unexpected error.", 500)
                                           )

    @on_exception(expo, RateLimitException, max_tries=10)
    @limits(calls=50, period=1)
    @limits(calls=1000, period=86400)
    def animal_types(self, types: AnimalTypes = None) -> dict:
        r"""
        Returns data on an animal type, or types available from the Petfinder API. This data includes the
        available type's coat names and colors, gender and other specific information relevant to the
        specified type(s). The animal type must be of 'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird',
        'scales-fins-other', 'barnyard'.

        Parameters
        ----------
        types : str, list or tuple, optional
            Specifies the animal type or types to return. Can be a string representing a single animal type, or a
            tuple or list of animal types if more than one type is desired. If not specified, all animal types are
            returned.

        Raises
        ------
        ValueError
            Raised when the :code:`types` parameter receives an invalid animal type.
        TypeError
            If the :code:`types` is not given either a str, list or tuple, or None, a :code:`TypeError` will be
            raised.

        Returns
        -------
        dict
            Dictionary object representing JSON data returned from the Petfinder API.

        Examples
        --------
        # Create an authenticated connection to the Petfinder API.
        >>> pf = Petfinder(key=key, secret=secret)
        # Get all available animal types and their associated data.
        >>> all_types = pf.animal_types()
        # Returning data for a single animal type.
        >>> dogs = pf.animal_types('dog')
        # Getting multiple animal types at once.
        >>> cat_dog_rabbit_types = pf.animal_types(['cat', 'dog', 'rabbit'])

        """
        if types is not None:
            type_check = types
            if isinstance(types, str):
                type_check = [types]
            diff = set(type_check).difference(('dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird',
                                               'scales-fins-other', 'barnyard'))
            if len(diff) > 0:
                raise ValueError("animal types must be of the following 'dog', 'cat', 'rabbit', "
                                 "'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard'")

        if types is None:
            url = urljoin(self._host, 'types')

            r = self._get_result(url,
                                 headers={
                                     'Authorization': 'Bearer ' + self._access_token
                                 })

            result = r.json()

        elif isinstance(types, str):
            url = urljoin(self._host, 'types/{type}'.format(type=types))

            r = self._get_result(url,
                                 headers={
                                     'Authorization': 'Bearer ' + self._access_token
                                 })

            result = r.json()

        elif isinstance(types, (tuple, list)):
            types_collection = []

            for t in types:
                url = urljoin(self._host, 'types/{type}'.format(type=t))

                r = self._get_result(url,
                                     headers={
                                         'Authorization': 'Bearer ' + self._access_token
                                     })

                types_collection.append(r.json()['type'])

            result = {'types': types_collection}

        else:
            raise TypeError('types parameter must be either None, str, list or tuple')

        return result

    @on_exception(expo, RateLimitException, max_tries=10)
    @limits(calls=50, period=1)
    @limits(calls=1000, period=86400)
    def breeds(self, types: AnimalTypes = None,
               return_df: bool = False, raw_results: bool = False) -> dict:
        r"""
        Returns breed names of specified animal type, or types.

        Parameters
        ----------
        types :  str, list or tuple, optional
            String representing a single animal type or a list or tuple of a collection of animal types. If not
            specified, all available breeds for each animal type is returned. The animal type must be of 'dog',
            'cat', 'rabbit', 'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard'.
        return_df : boolean, default False
            If :code:`True`, the result set will be coerced into a pandas :code:`DataFrame` with two columns,
            breed and name. If :code:`return_df` is set to :code:`True`, it will override the :code:`raw_result`
            parameter if it is also set to :code:`True` and return a pandas :code:`DataFrame`.
        raw_results: boolean, default False
            The PetFinder API :code:`breeds` endpoint returns some extraneous data in its result set along with the
            breed names of the specified animal type(s). If :code:`raw_results` is :code:`False`, the method will
            return a cleaner JSON object result set with the extraneous data removed. This parameter can be set to
            :code:`True` for those interested in retrieving the entire result set. If the parameter :code:`return_df`
            is set to :code:`True`, a pandas :code:`DataFrame` will be returned regardless of the value specified for
            the :code:`raw_result` parameter.

        Raises
        ------
        ValueError
            Raised when the :code:`types` parameter receives an invalid animal type.
        TypeError
            If the :code:`types` is not given either a str, list or tuple, or None, a :code:`TypeError` will be
            raised.

        Returns
        -------
        dict or pandas DataFrame
            If the parameter :code:`return_df` is :code:`False`, a dictionary object representing the JSON data
            returned from the Petfinder API is returned. If :code:`return_df=True`, the resulting dictionary is
            coerced into a pandas DataFrame. Note if :code:`return_df=True`, the parameter :code:`raw_results` is
            overridden.

        Examples
        --------
        # Create an authenticated connection to the Petfinder API.
        >>> pf = Petfinder(key=key, secret=secret)
        # Return all cat and dog breeds.
        >>> cat_breeds = pf.breeds('cat')
        >>> dog_breeds = pf.breeds('dog')
        # All available breeds or multiple breeds can also be returned.
        >>> all_breeds = pf.breeds()
        >>> cat_dog_rabbit = pf.breeds(types=['cat', 'dog', 'rabbit'])
        # The `breeds` method can also be set to coerce the returned JSON results into a pandas DataFrame by setting
        # the parameter `return_df = True`.
        >>> cat_breeds_df = pf.breeds('cat', return_df = True)
        >>> all_breeds_df = pf.breeds(return_df = True)

        """
        if types is not None:
            type_check = types
            if isinstance(types, str):
                type_check = [types]
            diff = set(type_check).difference(('dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird',
                                               'scales-fins-other', 'barnyard'))
            if len(diff) > 0:
                raise ValueError("animal types must be of the following 'dog', 'cat', 'rabbit', "
                                 "'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard'")

        if types is None or isinstance(types, (list, tuple)):
            breeds = []

            if types is None:
                types = ('dog', 'cat', 'rabbit', 'small-furry',
                         'horse', 'bird', 'scales-fins-other', 'barnyard')

            for t in types:
                url = urljoin(self._host, 'types/{type}/breeds'.format(type=t))

                r = self._get_result(url,
                                     headers={
                                         'Authorization': 'Bearer ' + self._access_token
                                     })
                breeds.append({t: r.json()})

            result = {'breeds': breeds}

        elif isinstance(types, str):
            url = urljoin(self._host, 'types/{type}/breeds'.format(type=types))

            r = self._get_result(url,
                                 headers={
                                     'Authorization': 'Bearer ' + self._access_token
                                 })
            result = r.json()

        else:
            raise TypeError('types parameter must be either None, str, list or tuple')

        if return_df:
            raw_results = True
            df_results = []
            if isinstance(types, (tuple, list)):
                for t in range(0, len(types)):
                    df_results.append(json_normalize(result['breeds'][t][types[t]]['breeds']))
            else:
                df_results.append(json_normalize(result['breeds']))
            df_results = pd.concat(df_results)
            df_results.rename(columns={'_links.type.href': 'breed'}, inplace=True)
            df_results['breed'] = df_results['breed'].str.replace('/v2/types/', '').str.capitalize()

            result = df_results

        if not raw_results:
            json_result = {
                'breeds': {

                }
            }

            if isinstance(types, (tuple, list)):
                for t in range(0, len(types)):
                    json_result['breeds'][types[t]] = []

                    for breed in result['breeds'][t][types[t]]['breeds']:
                        json_result['breeds'][types[t]].append(breed['name'])

            else:
                json_result['breeds'][types] = []

                for breed in result['breeds']:
                    json_result['breeds'][types].append(breed['name'])

            result = json_result

        return result

    @on_exception(expo, RateLimitException, max_tries=10)
    @limits(calls=50, period=1)
    @limits(calls=1000, period=86400)
    def animals(self, animal_id: PetfinderID = None,
                animal_type: str = None,
                breed: AnimalFeatures = None,
                size: AnimalFeatures = None,
                gender: AnimalFeatures = None,
                age: AnimalFeatures = None,
                color: str = None,
                coat: AnimalFeatures = None,
                status: str = None,
                name: str = None,
                organization_id: AnimalFeatures = None,
                location: str = None,
                distance: int = None,
                good_with_children: bool = None,
                good_with_dogs: bool = None,
                good_with_cats: bool = None,
                house_trained: bool = None,
                declawed: bool = None,
                special_needs: bool = None,
                before_date: Date = None,
                after_date: Date = None,
                sort: str = None,
                pages: int = 1,
                results_per_page: int = 20,
                return_df: bool = False) -> Animals:
        r"""
        Returns adoptable animal data from Petfinder based on specified criteria.

        Parameters
        ----------
        animal_id : int, tuple or list of int, optional
            Integer or list or tuple of integers representing animal IDs obtained from Petfinder. When
            :code:`animal_id` is specified, the other function parameters are overridden. If :code:`animal_id`
            is not specified, a search of animals on Petfinder matching given criteria is performed.
        animal_type : {'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard'}, str, optional
            String representing desired animal type to search. If specified, must be one of 'dog', 'cat', 'rabbit',
            'small-furry', 'horse', 'bird', 'scales-fins-other', or 'barnyard'.
        breed: str, tuple or list of str, optional
            String or tuple or list of strings of desired animal type breed to search. Available animal breeds in
            the Petfinder database can be found using the :code:`breeds()` method.
        size: {'small', 'medium', 'large', 'xlarge'}, str, tuple or list of str, optional
            String or tuple or list of strings of desired animal sizes to return. The specified size(s) must be one
            of 'small', 'medium', 'large', or 'xlarge'.
        gender : {'male', 'female', 'unknown'} str, tuple or list of str, optional
            String or tuple or list of strings representing animal genders to return. Must be of 'male', 'female',
            or 'unknown' if specified.
        age : {'baby', 'young', 'adult', 'senior'} str, tuple or list of str, optional
            String or tuple or list of strings specifying animal age(s) to return from search. Must be of 'baby',
            'young', 'adult', 'senior' if specified.
        color : str, optional
            String representing specified animal 'color' to search. Colors for each available animal type in the
            Petfinder database can be found using the :code:`animal_types()` method.
        coat : {'short', 'medium', 'long', 'wire', 'hairless', 'curly'}, str, tuple or list of str, optional
            Desired coat(s) to return. Must be of 'short', 'medium', 'long', 'wire', 'hairless', or 'curly'.
        status : {'adoptable', 'adopted', 'found'} str, optional
            Animal status to filter search results. If specified, must be one of 'adoptable', 'adopted', or 'found'.
        name : str, optional
            Searches for animal names matching or partially matching name.
        organization_id : str, tuple or list of str, optional
            Returns animals associated with given :code:`organization_id`. Can be a str or a tuple or list of str
            representing multiple organizations.
        location : str, optional
            Returns results by specified location. Must be in the format 'city, state' for city-level results,
            'latitude, longitude' for lat-long results, or 'postal code'.
        distance : int, optional
            Returns results within the distance of the specified location. If not given, defaults to 100 miles.
            Maximum distance range is 500 miles.
        good_with_children : bool, optional
            Filters animals that have been designated as being good with children.
        good_with_cats : bool, optional
            Filters the returned animals by those who have been flagged as being good with cats.
        good_with_dogs : bool, optional
            Returns results restricted to animals who have been flagged as being good with dogs.
        declawed : bool, optional
            Filters results for animals that have been declawed.
        special_needs : bool, optional
            Returns animals that have special needs.
        house_trained : bool, optional
            If specified, only returns animals that are listed as house-trained.
        before_date : str, datetime
            Returns results that have been published before the specified datetime. Must be a valid ISO8601 date-time
            string or a datetime object.
        after_date : str, datetime
            Returns results that have been published after the specified datetime. Must be a valid ISO8601 date-time
            string or a datetime object.
        sort : {'recent', '-recent', 'distance', '-distance'}, str, optional
            Sorts by specified attribute. Leading dashes represents a reverse-order sort. Must be one of 'recent',
            '-recent', 'distance', or '-distance'.
        pages : int, default 1
            Specifies which page of results to return. Defaults to the first page of results. If set to :code:`None`,
            all results will be returned.
        results_per_page : int, default 20
            Number of results to return per page. Defaults to 20 results and cannot exceed 100 results per page.
        return_df : boolean, default False
            If :code:`True`, the results will be coerced into a pandas DataFrame.

        Returns
        -------
        dict or pandas DataFrame
            Dictionary object representing the returned JSON object from the Petfinder API. If :code:`return_df=True`,
            the results are returned as a pandas DataFrame.

        Examples
        --------
        # Create an authenticated connection to the Petfinder API.
        >>> pf = Petfinder(key=key, secret=secret)
        # Getting first 20 results without any search criteria
        >>> animals = pf.animals()
        # Extracting data on specific animals with animal_ids
        >>> animal_ids = []
        >>> for i in animals['animals'][0:3]:
        >>>    animal_ids.append(i['id'])
        >>> animal_data = pf.animals(animal_id=animal_ids)
        # Returning a pandas DataFrame of the first 150 animal results
        >>> animals = pf.animals(results_per_page=50, pages=3, return_df=True)

        """
        if before_date:
            if isinstance(before_date, str):
                try:
                    before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            before_date = before_date.astimezone().replace(microsecond=0).isoformat()

        if after_date:
            if isinstance(after_date, str):
                try:
                    after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            after_date = after_date.astimezone().replace(microsecond=0).isoformat()

        if after_date is not None and before_date is not None:
            if before_date < after_date:
                raise ValueError('before_date parameter must be more recent than after_date parameter.')

        if animal_id is not None:
            url = urljoin(self._host, 'animals/{id}')
            if isinstance(animal_id, (tuple, list)):
                animals = []
                for ani_id in animal_id:
                    try:
                        r = self._get_result(url.format(id=ani_id),
                                             headers={
                                                 'Authorization': 'Bearer ' + self._access_token
                                             })

                        animal_data = r.json()['animal']
                        animal_data['response'] = 200
                    except PetfinderResourceNotFound:
                        animal_data = {
                            'id': ani_id,
                            'response': 404
                        }
                    animals.append(animal_data)
            else:
                try:
                    r = self._get_result(url.format(id=animal_id),
                                         headers={
                                             'Authorization': 'Bearer ' + self._access_token
                                         })
                    animals = r.json()['animal']
                    animals['response'] = 200
                except PetfinderResourceNotFound:
                    animals = {
                        'id': animal_id,
                        'response': 404
                    }

        else:
            url = urljoin(self._host, 'animals/')

            if animal_type:  # Petfinder API does not return correct results for animal_type otherwise
                url += '?type={}'.format(animal_type)

            params = _parameters(animal_type=animal_type,
                                 breed=breed,
                                 size=size,
                                 gender=gender,
                                 age=age,
                                 color=color,
                                 coat=coat,
                                 status=status,
                                 name=name,
                                 organization_id=organization_id,
                                 location=location,
                                 distance=distance,
                                 sort=sort,
                                 results_per_page=results_per_page,
                                 before_date=before_date,
                                 after_date=after_date,
                                 good_with_cats=good_with_cats,
                                 good_with_children=good_with_children,
                                 good_with_dogs=good_with_dogs,
                                 house_trained=house_trained,
                                 declawed=declawed,
                                 special_needs=special_needs)

            if not pages:
                params['limit'] = 100
                params['page'] = 1

                r = self._get_result(url,
                                     headers={
                                         'Authorization': 'Bearer ' + self._access_token
                                     },
                                     params=params)

                animals = r.json()['animals']
                max_pages = r.json()['pagination']['total_pages']

                for page in range(2, max_pages + 1):
                    params['page'] = page
                    r = self._get_result(url,
                                         headers={
                                             'Authorization': 'Bearer ' + self._access_token
                                         },
                                         params=params)

                    if isinstance(r.json(), dict):
                        if 'animals' in r.json().keys():
                            for i in r.json()['animals']:
                                animals.append(i)

            else:
                pages += 1
                params['page'] = 1

                r = self._get_result(url,
                                     headers={
                                         'Authorization': 'Bearer ' + self._access_token
                                     },
                                     params=params)

                animals = r.json()['animals']
                max_pages = r.json()['pagination']['total_pages']

                if pages > int(max_pages):
                    pages = max_pages

                for page in range(2, pages):
                    params['page'] = page
                    r = self._get_result(url,
                                         headers={
                                             'Authorization': 'Bearer ' + self._access_token
                                         },
                                         params=params)

                    if isinstance(r.json(), dict):
                        if 'animals' in r.json().keys():
                            for i in r.json()['animals']:
                                animals.append(i)

        animals = {
            'animals': animals
        }

        if return_df:
            animals = _coerce_to_dataframe(animals)

        return animals

    @on_exception(expo, RateLimitException, max_tries=10)
    @limits(calls=50, period=1)
    @limits(calls=1000, period=86400)
    def organizations(self,
                      organization_id: PetfinderID = None,
                      name: str = None,
                      location: str = None,
                      distance: int = None,
                      state: str = None,
                      country: str = None,
                      query: str = None,
                      sort: str = None,
                      results_per_page: int = 20,
                      pages: int = 1,
                      return_df: bool = False):
        r"""
        Returns data on an animal welfare organization, or organizations, based on specified criteria.

        Parameters
        ----------
        organization_id : str, tuple or list of str, optional
            Returns results for specified :code:`organization_id`. Can be a str or a tuple or list of str
            representing multiple organizations.
        name : str, optional
            Returns results matching or partially matching organization name.
        location : str, optional
            Returns results by specified location. Must be in the format 'city, state' for city-level results,
            'latitude, longitude' for lat-long results, or 'postal code'.
        distance : int, optional
            Returns results within the distance of the specified location. If not given, defaults to 100 miles.
            Maximum distance range is 500 miles.
        state : str, optional
            Filters the results by the selected state. Must be a two-letter state code abbreviation of the state
            name, such as 'WA' for Washington or 'NY' for New York.
        country : {'US', 'CA'}, optional
            Filters results to specified country. Must be a two-letter abbreviation of the country and is limited
            to the United States and Canada.
        query : str, optional
            Search matching and partially matching name, city or state.
        sort : {'recent', '-recent', 'distance', '-distance'}, str, optional
            Sorts by specified attribute. Leading dashes represents a reverse-order sort. Must be one of 'recent',
            '-recent', 'distance', or '-distance'.
        pages : int, default 1
            Specifies which page of results to return. Defaults to the first page of results. If set to :code:`None`,
            all results will be returned.
        results_per_page : int, default 20
            Number of results to return per page. Defaults to 20 results and cannot exceed 100 results per page.
        return_df : boolean, default False
            If :code:`True`, the results will be coerced into a pandas DataFrame.

        Returns
        -------
        dict or pandas DataFrame
            Dictionary object representing the returned JSON object from the Petfinder API. If :code:`return_df=True`,
            the results are returned as a pandas DataFrame.

        Examples
        --------
        # Create an authenticated connection to the Petfinder API.
        >>> pf = Petfinder(key=key, secret=secret)
        # Return the first 1,000 animal welfare organizations as a pandas DataFrame
        >>> organizations = pf.organizations(results_per_page=100, pages=10, return_df=True)
        # Get organizations in the state of Washington
        >>> wa_organizations = pf.organizations(state='WA')

        """
        if organization_id is not None:
            url = urljoin(self._host, 'organizations/{id}')
            if isinstance(organization_id, (tuple, list)):
                organizations = []
                for org_id in organization_id:
                    org = self._get_org(url=url, org_id=org_id)
                    organizations.append(org)
            else:
                organizations = self._get_org(url=url, org_id=organization_id)
        else:
            url = urljoin(self._host, 'organizations/')
            params = _parameters(name=name, location=location, distance=distance,
                                 state=state, country=country, query=query, sort=sort,
                                 results_per_page=results_per_page)
            if pages is None:
                params['limit'] = 100
                params['page'] = 1
                r = self._get_result(url,
                                     headers={
                                         'Authorization': 'Bearer ' + self._access_token
                                     },
                                     params=params)
                organizations = r.json()['organizations']
                max_pages = r.json()['pagination']['total_pages']
                for page in range(2, max_pages + 1):
                    params['page'] = page
                    r = self._get_result(url,
                                         headers={
                                             'Authorization': 'Bearer ' + self._access_token
                                         },
                                         params=params)
                    if isinstance(r.json(), dict):
                        if 'organizations' in r.json().keys():
                            for i in r.json()['organizations']:
                                organizations.append(i)
            else:
                pages += 1
                params['page'] = 1
                r = self._get_result(url,
                                     headers={
                                         'Authorization': 'Bearer ' + self._access_token
                                     },
                                     params=params)
                organizations = r.json()['organizations']
                max_pages = r.json()['pagination']['total_pages']

                if pages > int(max_pages):
                    pages = max_pages

                for page in range(2, pages):
                    params['page'] = page
                    r = self._get_result(url,
                                         headers={
                                             'Authorization': 'Bearer ' + self._access_token
                                         },
                                         params=params)
                    if isinstance(r.json(), dict):
                        if 'organizations' in r.json().keys():
                            for i in r.json()['organizations']:
                                organizations.append(i)

        organizations = {
            'organizations': organizations
        }

        if return_df:
            organizations = _coerce_to_dataframe(organizations)

        return organizations

    def _get_org(self, url, org_id):
        try:
            r = self._get_result(url.format(id=org_id),
                                 headers={
                                     'Authorization': 'Bearer ' + self._access_token
                                 })

            org = r.json()['organization']
            org['response'] = 200
        except PetfinderResourceNotFound:
            org = {
                'id': org_id,
                'response': 404
            }
        return org

    import requests

    def _get_result(self, url, headers, params=None, max_retries=3):
        def handle_response(r):
            if r.status_code == 200:
                return r
            elif r.status_code == 400:
                raise PetfinderInvalidParameters(
                    message='There are invalid parameters in the API query.',
                    err=r.json().get('invalid-params')
                )
            elif r.status_code == 401:
                if r.json().get('detail') == 'Access token invalid or expired':
                    self._access_token = self._authenticate()
                    return self._get_result(url, headers, params)
                else:
                    raise PetfinderInvalidCredentials(
                        message='Invalid Credentials',
                        err=(r.reason, r.status_code)
                    )
            elif r.status_code == 403:
                raise PetfinderInsufficientAccess(
                    message='Insufficient Access',
                    err=(r.reason, r.status_code)
                )
            elif r.status_code == 404:
                raise PetfinderResourceNotFound(
                    message='Requested Resource not Found',
                    err=(r.reason, r.status_code)
                )
            elif r.status_code == 429:
                raise PetfinderRateLimitExceeded(
                    message='Daily Rate Limit Exceeded. Resets at 12:00am UTC',
                    err=(r.reason, r.status_code)
                )
            elif r.status_code == 500:
                return None
            else:
                raise PetfinderUnexpectedError(
                    message='The Petfinder API encountered an unexpected error.',
                    err=(r.reason, r.status_code)
                )
        response = None
        for attempt in range(1, max_retries + 1):
            response = requests.get(url, headers=headers, params=params)
            result = handle_response(response)

            if result:
                return result
            elif response.status_code == 500:
                print(f'Attempt {attempt} of {max_retries} failed with status 500. Retrying...')
                if attempt == max_retries:
                    raise PetfinderUnexpectedError(
                        message='The Petfinder API encountered an unexpected error after maximum retries.',
                        err=(response.reason, response.status_code)
                    )
            else:
                break

        return response


#################################################################################################################
#
# Internal helper functions
#
#################################################################################################################


def _parameters(breed: AnimalFeatures = None,
                size: AnimalFeatures = None,
                gender: AnimalFeatures = None,
                color: str = None,
                coat: AnimalFeatures = None,
                animal_type: str = None, 
                location: int = None,
                distance: int = None,
                state: str = None,
                country: str = None,
                query: str = None,
                sort: str = None,
                name: str = None,
                age: str = None,
                good_with_children: bool = None,
                good_with_dogs: bool = None,
                good_with_cats: bool = None,
                declawed: bool = None,
                house_trained: bool = None,
                special_needs: bool = None,
                before_date: Date = None,
                after_date: Date = None,
                animal_id: PetfinderID = None,
                organization_id: PetfinderID = None,
                status: str = None,
                results_per_page: int = None,
                page: int = None):
    r"""
    Internal function for determining which parameters have been passed and aligning them to their respective
    Petfinder API parameters.

    Parameters
    ----------
    breed: str, tuple or list of str, optional
        String or tuple or list of strings of desired animal type breed to search.
    size: {'small', 'medium', 'large', 'xlarge'}, str, tuple or list of str, optional
        String or tuple or list of strings of desired animal sizes to return. The specified size(s) must be one
        of 'small', 'medium', 'large', or 'xlarge'.
    gender: {'male', 'female', 'unknown'} str, tuple or list of str, optional
        String or tuple or list of strings representing animal genders to return. Must be of 'male', 'female',
        or 'unknown'.
    color : str, optional
        String representing specified animal 'color' to search. Colors for each available animal type in the
        Petfinder database can be found using the :code:`animal_types()` method.
    coat : {'short', 'medium', 'long', 'wire', 'hairless', 'curly'}, str, tuple or list of str, optional
        Desired coat(s) to return. Must be of 'short', 'medium', 'long', 'wire', 'hairless', or 'curly'.
    animal_type : {'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard'}, str, optional
        String representing desired animal type to search. Must be one of 'dog', 'cat', 'rabbit', 'small-furry',
        'horse', 'bird', 'scales-fins-other', or 'barnyard'.
    location : str, optional
        Returns results by specified location. Must be in the format 'city, state' for city-level results,
        'latitude, longitude' for lat-long results, or 'postal code'.
    distance : int, optional
        Returns results within the distance of the specified location. If not given, defaults to 100 miles.
        Maximum distance range is 500 miles.
    state : str, optional
        Filters the results by the selected state. Must be a two-letter state code abbreviation of the state
        name, such as 'WA' for Washington or 'NY' for New York.
    country : {'US', 'CA'}, str, optional
        Filters results to specified country. Must be a two-letter abbreviation of the country and is limited
        to the United States and Canada.
    query : str, optional
        Search matching and partially matching name, city or state.
    sort : {'recent', '-recent', 'distance', '-distance'}, str, optional
            Sorts by specified attribute. Leading dashes represents a reverse-order sort. Must be one of 'recent',
            '-recent', 'distance', or '-distance'.
    name : str, optional
        Name of animal or organization to search.
    age : {'baby', 'young', 'adult', 'senior'} str, tuple or list of str, optional
        String or tuple or list of strings specifying animal age(s) to return from search. Must be of 'baby',
        'young', 'adult', 'senior'.
    good_with_cats: bool, optional
        Filters returned animal results to animals that are designated as good with cats. Must be a boolean value
        (True, False) or a value that can be coerced to a boolean (1, 0).
    good_with_children: bool, optional
        Filters returned animal results to animals that are designated as good with children. Must be a boolean value
        (True, False) or a value that can be coerced to a boolean (1, 0).
    good_with_dogs: bool, optional
        Filters returned animal results to animals that are designated as good with dogs. Must be a boolean value
        (True, False) or a value that can be coerced to a boolean (1, 0).
    before_date: str, datetime, optional
        Returns results with a `published_at` datetime before the specified time. Must be a string in the form of
        'YYYY-MM-DD' or 'YYYY-MM-DD H:M:S' or a datetime object.
    after_date: str, datetime, optional
        Returns results with a `published_at` datetime after the specified time. Must be a string in the form of
        'YYYY-MM-DD' or 'YYYY-MM-DD H:M:S' or a datetime object.
    animal_id : int, tuple or list of int, optional
        Integer or list or tuple of integers representing animal IDs obtained from Petfinder.
    organization_id : str, tuple or list of str, optional
        Returns animals associated with given :code:`organization_id`. Can be a str or a tuple or list of str
        representing multiple organizations.
    status : {'adoptable', 'adopted', 'found'} str, optional
        Animal status to filter search results. Must be one of 'adoptable', 'adopted', or 'found'.
    results_per_page : int, default 20
        Number of results to return per page. Defaults to 20 results and cannot exceed 100 results per page.
    page : int, default 1
        Specifies which page of results to return. Defaults to the first page of results. If set to :code:`None`,
        all results will be returned.

    Returns
    -------
    dict
        Dictionary representing aligned parameters and headers for ingestion into the Petfinder API.

    """
    if isinstance(age, (list, tuple)):
        age = ','.join(age).replace(' ', '')
    if isinstance(gender, (list, tuple)):
        gender = ','.join(gender).replace(' ', '')
    if isinstance(status, (list, tuple)):
        status = ','.join(status).replace(' ', '')
    if isinstance(animal_type, (list, tuple)):
        animal_type = ','.join(animal_type).replace(' ', '')
    if isinstance(size, (list, tuple)):
        size = ','.join(size).replace(' ', '')
    if isinstance(coat, (list, tuple)):
        coat = ','.join(coat).replace(' ', '')

    if good_with_cats is not None:
        good_with_cats = int(good_with_cats)
    if good_with_children is not None:
        good_with_children = int(good_with_children)
    if good_with_dogs is not None:
        good_with_dogs = int(good_with_dogs)
    if declawed is not None:
        declawed = int(declawed)
    if house_trained is not None:
        house_trained = int(house_trained)
    if special_needs is not None:
        special_needs = int(special_needs)

    _check_parameters(
        animal_types=animal_type,
        size=size,
        gender=gender,
        age=age,
        coat=coat,
        status=status,
        distance=distance,
        sort=sort,
        limit=results_per_page,
        good_with_cats=good_with_cats,
        good_with_children=good_with_children,
        good_with_dogs=good_with_dogs,
        declawed=declawed,
        house_trained=house_trained,
        special_needs=special_needs
    )

    args = {
        'breed': breed,
        'size': size,
        'gender': gender,
        'age': age,
        'color': color,
        'coat': coat,
        'animal_type': animal_type,
        'location': location,
        'distance': distance,
        'state': state,
        'country': country,
        'query': query,
        'sort': sort,
        'name': name,
        'animal_id': animal_id,
        'organization': organization_id,
        'good_with_cats': good_with_cats,
        'good_with_children': good_with_children,
        'good_with_dogs': good_with_dogs,
        'house_trained': house_trained,
        'special_needs': special_needs,
        'declawed': declawed,
        'before': before_date,
        'after': after_date,
        'status': status,
        'limit': results_per_page,
        'page': page
    }

    args = {key: val for key, val in args.items() if val is not None}

    return args


def _check_parameters(
        animal_types: str = None,
        size: AnimalFeatures = None,
        gender: AnimalFeatures = None,
        age: AnimalFeatures = None,
        coat: AnimalFeatures = None,
        status: str = None,
        distance: int = None,
        good_with_children: bool = None,
        good_with_dogs: bool = None,
        good_with_cats: bool = None,
        declawed: bool = None,
        house_trained: bool = None,
        special_needs: bool = None,
        sort: str = None,
        limit: int = None):
    r"""
    Internal function for checking the passed parameters against valid options available in the Petfinder API.

    Parameters
    ----------
    animal_type : {'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard'}, str, optional
        String representing desired animal type to search. Must be one of 'dog', 'cat', 'rabbit', 'small-furry',
        'horse', 'bird', 'scales-fins-other', or 'barnyard'.
    size: {'small', 'medium', 'large', 'xlarge'}, str, tuple or list of str, optional
        String or tuple or list of strings of desired animal sizes to return. The specified size(s) must be one
        of 'small', 'medium', 'large', or 'xlarge'.
    gender: {'male', 'female', 'unknown'} str, tuple or list of str, optional
        String or tuple or list of strings representing animal genders to return. Must be of 'male', 'female',
        or 'unknown'.
    age : {'baby', 'young', 'adult', 'senior'} str, tuple or list of str, optional
        String or tuple or list of strings specifying animal age(s) to return from search. Must be of 'baby',
        'young', 'adult', 'senior'.
    coat : {'short', 'medium', 'long', 'wire', 'hairless', 'curly'}, str, tuple or list of str, optional
        Desired coat(s) to return. Must be of 'short', 'medium', 'long', 'wire', 'hairless', or 'curly'.
    status : {'adoptable', 'adopted', 'found'} str, optional
        Animal status to filter search results. Must be one of 'adoptable', 'adopted', or 'found'.
    distance : int, optional
        Returns results within the distance of the specified location. If not given, defaults to 100 miles.
        Maximum distance range is 500 miles.
    sort : {'recent', '-recent', 'distance', '-distance'}, str, optional
            Sorts by specified attribute. Leading dashes represents a reverse-order sort. Must be one of 'recent',
            '-recent', 'distance', or '-distance'.
    limit : int, default 20
        Number of results to return per page. Defaults to 20 results and cannot exceed 100 results per page.

    Raises
    ------
    ValueError

    Returns
    -------
    None
        If :code:`ValueError` is not raised, the function returns :code:`None` which signifies the passed API
        parameters are valid.

    """
    _animal_types = ('dog', 'cat', 'rabbit', 'small-furry',
                     'horse', 'bird', 'scales-fins-other', 'barnyard')
    _sizes = ('small', 'medium', 'large', 'xlarge')
    _genders = ('male', 'female', 'unknown')
    _ages = ('baby', 'young', 'adult', 'senior')
    _coats = ('short', 'medium', 'long', 'wire', 'hairless', 'curly')
    _status = ('adoptable', 'adopted', 'found')
    _sort = ('recent', '-recent', 'distance', '-distance')

    incorrect_values = {}

    if animal_types is not None and animal_types not in _animal_types:
        incorrect_values['animal_types'] = "animal types {types} is not valid. Animal types " \
                                           "must of the following: {animal_types}"\
            .format(types=animal_types,
                    animal_types=_animal_types)

    if size is not None:
        size_list = size.split(',')
        diff = list(set(size_list).difference(_sizes))

        if len(diff) > 0:
            incorrect_values['size'] = "sizes {sizes} are not valid. Sizes must be of the following: {size_list}"\
                .format(sizes=diff,
                        size_list=_sizes)

    if gender is not None:
        gender_list = gender.split(',')
        diff = list(set(gender_list).difference(_genders))

        if len(diff) > 0:
            incorrect_values['gender'] = "genders {genders} are not valid. Genders must be of the following: " \
                                         "{gender_list}"\
                .format(genders=diff,
                        gender_list=_genders)

    if age is not None:
        age_list = age.split(',')
        diff = list(set(age_list).difference(_ages))

        if len(diff) > 0:
            incorrect_values['age'] = "ages {age} are not valid. Ages must be of the following: " \
                                      "{ages_list}" \
                .format(age=diff,
                        ages_list=_ages)

    if coat is not None:
        coat_list = coat.split(',')
        diff = list(set(coat_list).difference(_coats))

        if len(diff) > 0:
            incorrect_values['coat'] = "coats {coats} are not valid. Coats must be of the following: " \
                                       "{coat_list}"\
                .format(coats=diff,
                        coat_list=_coats)

    if status is not None:
        status_list = status.split(',')
        diff = list(set(status_list).difference(_status))

        if len(diff) > 0:
            incorrect_values['status'] = "status {status} are not valid. Coats must be of the following: " \
                                       "{status_list}" \
                .format(status=diff,
                        status_list=_coats)

    if sort is not None and sort not in _sort:
        incorrect_values['sort'] = "sort order {sort} must be one of: {sort_list}"\
            .format(sort=sort,
                    sort_list=_sort)

    if distance is not None:
        if not 0 <= int(distance) <= 500:
            incorrect_values['distance'] = "distance cannot be greater than 500 or less than 0."

    if good_with_dogs is not None:
        if not isinstance(good_with_dogs, (bool, int)):
            incorrect_values['good_with_dogs'] = 'good_with_dogs must be a boolean (True, False, 1, or 0).'

    if good_with_cats is not None:
        if not isinstance(good_with_cats, (bool, int)):
            incorrect_values['good_with_cats'] = 'good_with_dogs must be a boolean (True, False, 1, or 0).'

    if good_with_children is not None:
        if not isinstance(good_with_children, (bool, int)):
            incorrect_values['good_with_children'] = 'good_with_dogs must be a boolean (True, False, 1, or 0).'

    if declawed is not None:
        if not isinstance(declawed, (bool, int)):
            incorrect_values['declawed'] = 'declawed must be a boolean (True, False, 1, or 0).'

    if house_trained is not None:
        if not isinstance(house_trained, (bool, int)):
            incorrect_values['house_trained'] = 'house_trained must be a boolean (True, False, 1, or 0).'

    if special_needs is not None:
        if not isinstance(special_needs, (bool, int)):
            incorrect_values['special_needs'] = 'house_trained must be a boolean (True, False, 1, or 0).'

    if limit is not None:
        if int(limit) > 100:
            incorrect_values['limit'] = "results per page cannot be greater than 100"

    if len(incorrect_values) > 0:
        errors = ''
        for k, v in incorrect_values.items():
            errors = errors + v + '\n'

        raise ValueError(errors)

    return None


def _coerce_to_dataframe(results):
    r"""
    Internal function for coercing results from the Petfinder API into a pandas DataFrame.

    Parameters
    ----------
    results: dict
        Dictionary object representing JSON results from the Petfinder API.

    Returns
    -------
    pandas DataFrame
        pandas DataFrame coerced from resulting JSON data returned from the Petfinder API

    """
    key = list(results.keys())[0]
    results_df = json_normalize(results[key])

    if key == 'animals':
        results_df['_links.organization.href'] = results_df['_links.organization.href']\
            .str.replace('/v2/organizations/', '')
        results_df['_links.self.href'] = results_df['_links.self.href'].str.replace('/v2/animals/', '')
        results_df['_links.type.href'] = results_df['_links.type.href'].str.replace('/v2/types/', '')

        results_df.rename(columns={'_links.organization.href': 'organization_id',
                                   '_links.self.href': 'animal_id',
                                   '_links.type.href': 'animal_type'}, inplace=True)

    if key == 'organizations':
        del results_df['_links.animals.href']
        results_df['_links.self.href'] = results_df['_links.self.href'].str.replace('/v2/organizations/', '')

        results_df.rename(columns={'_links.self.href': 'organization_id'}, inplace=True)

    return results_df
