# encoding=utf-8

r"""

The :code:`api.py` file stores all the :code:`Petfinder` class and all associated functions and methods for
interacting with the Petfinder API. Before getting started with :code:`petpy`, please be sure to obtain an
API and secret key from Petfinder by registering for an account on the Petfinder developers page at
https://www.petfinder.com/developers/

"""


from pandas import DataFrame
from pandas import json_normalize
import requests
from urllib.parse import urljoin

from petpy.exceptions import PetfinderInvalidCredentials, PetfinderInsufficientAccess, PetfinderResourceNotFound, \
    PetfinderUnexpectedError, PetfinderInvalidParameters

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
    host : str
        The base URL of the Petfinder API.
    key : str
        The key from the Petfinder API passed when the :code:`Petfinder` class is initialized.
    secret : str
        The secret key obtained from the Petfinder API passed when the :code:`Petfinder` class is initialized.
    auth : str
        The authorization token string returned when the connection to the Petfinder API is made with the specified
        :code:`key` and :code:`secret`.

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
    def __init__(self, key, secret):
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
        self._host = 'http://api.petfinder.com/v2/'
        self._auth = self._authenticate()

    def _authenticate(self):
        r"""
        Internal function for authenticating users to the Petfinder API.

        Raises
        ------

        Returns
        -------
        str
            Access token granted by the Petfinder API. The access token stays live for 3600 seconds, or one hour,
            at which point the user must reauthenticate.

        """
        endpoint = 'oauth2/token'

        url = urljoin(self._host, endpoint)

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.key,
            'client_secret': self.secret
        }

        r = requests.post(url, data=data)

        if r.status_code == 401:
            raise PetfinderInvalidCredentials(message=r.reason, err='Invalid Credentials')

        return r.json()['access_token']

    def animal_types(self, types=None):
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

            r = _get_result(url,
                            headers={
                                'Authorization': 'Bearer ' + self._auth
                            })

            result = r.json()

        elif isinstance(types, str):
            url = urljoin(self._host, 'types/{type}'.format(type=types))

            r = _get_result(url,
                            headers={
                                'Authorization': 'Bearer ' + self._auth
                            })

            result = r.json()

        elif isinstance(types, (tuple, list)):
            types_collection = []

            for t in types:
                url = urljoin(self._host, 'types/{type}'.format(type=t))

                r = _get_result(url,
                                headers={
                                    'Authorization': 'Bearer ' + self._auth
                                })

                types_collection.append(r.json()['type'])

            result = {'types': types_collection}

        else:
            raise TypeError('types parameter must be either None, str, list or tuple')

        return result

    def breeds(self, types=None, return_df=False, raw_results=False):
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

                r = _get_result(url,
                                headers={
                                    'Authorization': 'Bearer ' + self._auth
                                })
                _check_api_rate_exceeded(r.json())
                breeds.append({t: r.json()})

            result = {'breeds': breeds}

        elif isinstance(types, str):
            url = urljoin(self._host, 'types/{type}/breeds'.format(type=types))

            r = _get_result(url,
                            headers={
                                'Authorization': 'Bearer ' + self._auth
                            })
            _check_api_rate_exceeded(r.json())
            result = r.json()

        else:
            raise TypeError('types parameter must be either None, str, list or tuple')

        if return_df:
            raw_results = True

            df_results = DataFrame()

            if isinstance(types, (tuple, list)):

                for t in range(0, len(types)):
                    df_results = df_results.append(json_normalize(result['breeds'][t][types[t]]['breeds']))

            else:
                df_results = df_results.append(json_normalize(result['breeds']))

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

    def animals(self, animal_id=None, animal_type=None, breed=None, size=None, gender=None,
                age=None, color=None, coat=None, status=None, name=None, organization_id=None,
                location=None, distance=None, sort=None, pages=1, results_per_page=20, return_df=False):
        r"""
        Returns adoptable animal data from Petfinder based on specified criteria.

        Parameters
        ----------
        animal_id : int, tuple or list of int, optional
            Integer or list or tuple of integers representing animal IDs obtained from Petfinder. When
            :code:`animal_id` is specified, the other function parameters are overridden. If :code:`animal_id`
            is not specified, a search of animals on Petfinder matching given criteria is performed.
        animal_type : {'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard'}, str, optional
            String representing desired animal type to search. Must be one of 'dog', 'cat', 'rabbit', 'small-furry',
            'horse', 'bird', 'scales-fins-other', or 'barnyard'.
        breed: str, tuple or list of str, optional
            String or tuple or list of strings of desired animal type breed to search. Available animal breeds in
            the Petfinder database can be found using the :code:`breeds()` method.
        size: {'small', 'medium', 'large', 'xlarge'}, str, tuple or list of str, optional
            String or tuple or list of strings of desired animal sizes to return. The specified size(s) must be one
            of 'small', 'medium', 'large', or 'xlarge'.
        gender : {'male', 'female', 'unknown'} str, tuple or list of str, optional
            String or tuple or list of strings representing animal genders to return. Must be of 'male', 'female',
            or 'unknown'.
        age : {'baby', 'young', 'adult', 'senior'} str, tuple or list of str, optional
            String or tuple or list of strings specifying animal age(s) to return from search. Must be of 'baby',
            'young', 'adult', 'senior'.
        color : str, optional
            String representing specified animal 'color' to search. Colors for each available animal type in the
            Petfinder database can be found using the :code:`animal_types()` method.
        coat : {'short', 'medium', 'long', 'wire', 'hairless', 'curly'}, str, tuple or list of str, optional
            Desired coat(s) to return. Must be of 'short', 'medium', 'long', 'wire', 'hairless', or 'curly'.
        status : {'adoptable', 'adopted', 'found'} str, optional
            Animal status to filter search results. Must be one of 'adoptable', 'adopted', or 'found'.
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
        sort : {'recent', '-recent', 'distance', '-distance'}, optional
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
        max_page_warning = False

        if animal_id is not None:

            url = urljoin(self._host, 'animals/{id}')

            if isinstance(animal_id, (tuple, list)):

                animals = []

                for ani_id in animal_id:
                    r = _get_result(url.format(id=ani_id),
                                    headers={
                                        'Authorization': 'Bearer ' + self._auth
                                    })
                    _check_api_rate_exceeded(r.json())
                    animals.append(r.json()['animal'])

            else:
                r = _get_result(url.format(id=animal_id),
                                headers={
                                    'Authorization': 'Bearer ' + self._auth
                                })
                _check_api_rate_exceeded(r.json())
                animals = r.json()['animal']

        else:

            url = urljoin(self._host, 'animals/')

            if animal_type: # Petfinder API does not return correct results for animal_type otherwise
                    url += '?type={}'.format(animal_type)

            params = _parameters(animal_type=animal_type, breed=breed, size=size, gender=gender,
                                 age=age, color=color, coat=coat, status=status, name=name,
                                 organization_id=organization_id, location=location, distance=distance,
                                 sort=sort, results_per_page=results_per_page)

            if pages is None:
                params['limit'] = 100
                params['page'] = 1

                r = _get_result(url,
                                headers={
                                    'Authorization': 'Bearer ' + self._auth
                                },
                                params=params)
                _check_api_rate_exceeded(r.json())
                animals = r.json()['animals']
                max_pages = r.json()['pagination']['total_pages']
                max_pages = _check_pages_api_limit(max_pages)

                for page in range(2, max_pages + 1):

                    params['page'] = page

                    r = _get_result(url,
                                    headers={
                                        'Authorization': 'Bearer ' + self._auth
                                    },
                                    params=params)
                    if _check_api_rate_exceeded(r.json(), exit_loop=True):
                        break
                    if isinstance(r.json(), dict):
                        if 'animals' in r.json().keys():
                            for i in r.json()['animals']:
                                animals.append(i)

            else:
                pages += 1
                params['page'] = 1
                
                r = _get_result(url,
                                headers={
                                    'Authorization': 'Bearer ' + self._auth
                                },
                                params=params)

                _check_api_rate_exceeded(r.json())

                animals = r.json()['animals']
                max_pages = r.json()['pagination']['total_pages']

                pages = _check_pages_api_limit(pages)

                if pages > int(max_pages) + 1:
                    pages = max_pages
                    max_page_warning = True

                for page in range(2, pages):

                    params['page'] = page

                    r = _get_result(url,
                                    headers={
                                        'Authorization': 'Bearer ' + self._auth
                                    },
                                    params=params)
                    if _check_api_rate_exceeded(r.json(), exit_loop=True):
                        break
                    if isinstance(r.json(), dict):
                        if 'animals' in r.json().keys():
                            for i in r.json()['animals']:
                                animals.append(i)

        animals = {
            'animals': animals
        }

        if return_df:
            animals = _coerce_to_dataframe(animals)

        if max_page_warning:
            print('pages parameter exceeded maximum number of available pages available from the Petfinder API. As '
                  'a result, the maximum number of pages {max_page} was returned'.format(max_page=max_pages))

        return animals

    def organizations(self, organization_id=None, name=None, location=None, distance=None, state=None,
                      country=None, query=None, sort=None, results_per_page=20, pages=1, return_df=False):
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
        sort : {'recent', '-recent', 'distance', '-distance'}, optional
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
        max_page_warning = False

        if organization_id is not None:

            url = urljoin(self._host, 'organizations/{id}')

            if isinstance(organization_id, (tuple, list)):

                organizations = []

                for org_id in organization_id:
                    r = _get_result(url.format(id=org_id),
                                    headers={
                                        'Authorization': 'Bearer ' + self._auth
                                    })

                    organizations.append(r.json()['organization'])

            else:
                r = _get_result(url.format(id=organization_id),
                                headers={
                                    'Authorization': 'Bearer ' + self._auth
                                })

                organizations = r.json()['organization']

        else:

            url = urljoin(self._host, 'organizations/')

            params = _parameters(name=name, location=location, distance=distance,
                                 state=state, country=country, query=query, sort=sort,
                                 results_per_page=results_per_page)

            if pages is None:
                params['limit'] = 100
                params['page'] = 1

                r = _get_result(url,
                                headers={
                                    'Authorization': 'Bearer ' + self._auth
                                },
                                params=params)
                _check_api_rate_exceeded(r.json())
                organizations = r.json()['organizations']

                max_pages = r.json()['pagination']['total_pages']
                max_pages = _check_pages_api_limit(max_pages)

                for page in range(2, max_pages + 1):

                    params['page'] = page

                    r = _get_result(url,
                                    headers={
                                        'Authorization': 'Bearer ' + self._auth
                                    },
                                    params=params)
                    if _check_api_rate_exceeded(r.json(), exit_loop=True):
                        break
                    if isinstance(r.json(), dict):
                        if 'organizations' in r.json().keys():
                            for i in r.json()['organizations']:
                                organizations.append(i)

            else:
                pages += 1
                params['page'] = 1

                r = _get_result(url,
                                headers={
                                    'Authorization': 'Bearer ' + self._auth
                                },
                                params=params)
                _check_api_rate_exceeded(r.json())
                organizations = r.json()['organizations']
                max_pages = r.json()['pagination']['total_pages']
                pages = _check_pages_api_limit(pages)

                if pages > int(max_pages):
                    pages = max_pages
                    max_page_warning = True

                for page in range(2, pages):

                    params['page'] = page

                    r = _get_result(url,
                                    headers={
                                        'Authorization': 'Bearer ' + self._auth
                                    },
                                    params=params)
                    if _check_api_rate_exceeded(r.json(), exit_loop=True):
                        break
                    if isinstance(r.json(), dict):
                        if 'organizations' in r.json().keys():
                            for i in r.json()['organizations']:
                                organizations.append(i)

        organizations = {
            'organizations': organizations
        }

        if return_df:
            organizations = _coerce_to_dataframe(organizations)

        if max_page_warning:
            print('pages parameter exceeded maximum number of available pages available from the Petfinder API. As '
                  'a result, the maximum number of pages {max_page} was returned'.format(max_page=max_pages))

        return organizations


#################################################################################################################
#
# Internal helper functions
#
#################################################################################################################


def _get_result(url, headers, params=None):

    r = requests.get(url,
                     headers=headers,
                     params=params)

    if r.status_code == 400:
        raise PetfinderInvalidParameters(message='There are invalid parameters in the API query.',
                                         err=r.json()['invalid-params'])

    if r.status_code == 401:
        raise PetfinderInvalidCredentials(message='Invalid Credentials',
                                          err=(r.reason, r.status_code))

    if r.status_code == 403:
        raise PetfinderInsufficientAccess(message='Insufficient Access',
                                          err=(r.reason, r.status_code))

    if r.status_code == 404:
        raise PetfinderResourceNotFound(message='Requested Resource not Found',
                                        err=(r.reason, r.status_code))

    if r.status_code == 500:
        raise PetfinderUnexpectedError(message='The Petfinder API encountered an unexpected error.',
                                       err=(r.reason, r.status_code))

    return r


def _parameters(breed=None, size=None, gender=None, color=None, coat=None, animal_type=None, location=None,
                distance=None, state=None, country=None, query=None, sort=None, name=None, age=None,
                animal_id=None, organization_id=None, status=None, results_per_page=None, page=None):
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
    country : {'US', 'CA'}, optional
        Filters results to specified country. Must be a two-letter abbreviation of the country and is limited
        to the United States and Canada.
    query : str, optional
        Search matching and partially matching name, city or state.
    sort : {'recent', '-recent', 'distance', '-distance'}, optional
            Sorts by specified attribute. Leading dashes represents a reverse-order sort. Must be one of 'recent',
            '-recent', 'distance', or '-distance'.
    name : str, optional
        Name of animal or organization to search.
    age : {'baby', 'young', 'adult', 'senior'} str, tuple or list of str, optional
        String or tuple or list of strings specifying animal age(s) to return from search. Must be of 'baby',
        'young', 'adult', 'senior'.
    animal_id : int, tuple or list of int, optional
        Integer or list or tuple of integers representing animal IDs obtained from Petfinder.
    organization_id : str, tuple or list of str, optional
        Returns animals associated with given :code:`organization_id`. Can be a str or a tuple or list of str
        representing multiple organizations.
    status : {'adoptable', 'adopted', 'found'} str, optional
        Animal status to filter search results. Must be one of 'adoptable', 'adopted', or 'found'.
    results_per_page : int, default 20
        Number of results to return per page. Defaults to 20 results and cannot exceed 100 results per page.
    pages : int, default 1
        Specifies which page of results to return. Defaults to the first page of results. If set to :code:`None`,
        all results will be returned.

    Returns
    -------
    dict
        Dictionary representing aligned parameters and headers for ingestion into the Petfinder API.

    """
    _check_parameters(animal_types=animal_type, size=size, gender=gender, age=age, coat=coat, status=status,
                      distance=distance, sort=sort, limit=results_per_page)

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
        'status': status,
        'limit': results_per_page,
        'page': page
    }

    args = {key: val for key, val in args.items() if val is not None}

    return args


def _check_parameters(animal_types=None, size=None, gender=None, age=None, coat=None, status=None,
                      distance=None, sort=None, limit=None):
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
    sort : {'recent', '-recent', 'distance', '-distance'}, optional
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
        if isinstance(size, str):
            size = [size]
        diff = set(size).difference(_sizes)

        if len(diff) > 0:
            incorrect_values['size'] = "sizes {sizes} are not valid. Sizes must be of the following: {size_list}"\
                .format(sizes=diff,
                        size_list=_sizes)

    if gender is not None:
        if isinstance(gender, str):
            gender = [gender]
        diff = set(gender).difference(_genders)

        if len(diff) > 0:
            incorrect_values['gender'] = "genders {genders} are not valid. Genders must be of the following: " \
                                         "{gender_list}"\
                .format(genders=diff,
                        gender_list=_genders)

    if age is not None:
        if isinstance(age, str):
            age = [age]
        diff = set(age).difference(_ages)

        if len(diff) > 0:
            incorrect_values['age'] = "ages {age} are not valid. Ages must be of the following: " \
                                      "{ages_list}"\
                .format(age=diff,
                        ages_list=_ages)

    if coat is not None:
        if isinstance(coat, str):
            coat = [coat]
        diff = set(coat).difference(_coats)

        if len(diff) > 0:
            incorrect_values['coat'] = "coats {coats} are not valid. Coats must be of the following: " \
                                       "{coat_list}"\
                .format(coats=diff,
                        coat_list=_coats)

    if status is not None and status not in _status:
        incorrect_values['status'] = "animal status {status} is not valid. Status must be of the following: " \
                                     "{statuses}".format(status=status,
                                                         statuses=_status)

    if sort is not None and sort not in _sort:
        incorrect_values['sort'] = "sort order {sort} must be one of: {sort_list}"\
            .format(sort=sort,
                    sort_list=_sort)

    if distance is not None:
        if not 0 <= int(distance) <= 500:
            incorrect_values['distance'] = "distance cannot be greater than 500 or less than 0."

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


def _check_pages_api_limit(max_pages):
    r"""
    Internal function for checking number of pages requested to comply with api quota.

    Parameters
    ----------
    max_pages: int
        max number of pages that returned from the Petfinder API.

    Returns
    -------
    integer
        either the original max_pages if the user got an advanced quota or 10,000 which is the current normal quota for api requests

    """
    if max_pages > 10000: # Limit for api calls per day
        ans = input('''Total pages requested is {} which exceeds the daily API requests quota by PetFinder,
                        do you want to limit the pages to 10,000 only? y|n '''.format(max_pages))
        if ans.lower() in ['y', 'yes']:
            max_pages = 10000
        elif ans.lower() not in ['n', 'no']:
            raise ValueError('Only y|n accepted as answers')

    return max_pages


def _check_api_rate_exceeded(r, exit_loop=False):
    r"""
    Internal function for catching api exceeded error.

    Parameters
    ----------
    r: dict
        response.json() returned from the Petfinder API.

    Returns
    -------
    None
        raises an error and terminates the program

    """
    if isinstance(r, dict):
        if 'status' in r.keys() and r['status'] == 429:
            if exit_loop:
                print(r['title'])
                return True
            else:
                raise RuntimeError(r['title'])
