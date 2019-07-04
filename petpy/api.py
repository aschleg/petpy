# encoding=utf-8


import pandas as pd
from pandas import concat
from pandas.io.json import json_normalize
import requests
from urllib.parse import urljoin

from petpy.lib import parameters, query, return_multiple_get_calls


class Petfinder(object):
    r"""
    Wrapper class for the PetFinder API.

    Attributes
    ----------
    host : str
        The base URL of the Petfinder API.
    key : str
        The API key.
    secret: str
        The secret key.

    Methods
    -------
    animal_types(types, return_df=False)
        Returns data on an animal type, or types available from the PetFinder API.
    breed_list(animal, outputformat='json')
        Returns the breeds of :code:`animal`
    pet_find(location=None, animal=None, breed=None, size=None, sex=None, age=None, offset=None, count=None, output=None, outputformat='json')
        Returns a collection of pet records matching input parameters.
    pet_get(petId, outputformat='json')
        Returns a single pet record for the given :code:`petId`
    shelter_find(location, name=None, offset=None, count=None, outputformat='json')
        Gets a collection of shelter records matching input parameters.
    shelter_get(shelterId, outputformat='json')
        Gets the record for the given :code:`shelterID`
    shelter_get_pets(shelterId, status=None, offset=None, count=None, output=None, outputformat='json')
        Outputs a collection of pet IDs or records for the shelter specified by :code:`shelterID`
    shelter_list_by_breed(animal, breed, offset=None, count=None, outputformat='json')
        Returns shelterIDs listing animals of the specified :code:`breed`

    """
    def __init__(self, key, secret):
        r"""

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
        self.host = 'http://api.petfinder.com/v2/'
        self.auth = self._authenticate()

        self._available_types = ('dog', 'cat', 'rabbit', 'small-furry',
                                 'horse', 'bird', 'scales-fins-other', 'barnyard')

    def _authenticate(self):
        r"""
        Internal function for authenticating users to the Petfinder API.

        Raises
        ------
        HTTPError
            Raised when the authentication to the Petfinder API is unsuccessful.

        Returns
        -------
        str
            Access token granted by the Petfinder API. The access token stays live for 3600 seconds, or one hour,
            at which point the user must reauthenticate.

        """
        endpoint = 'oauth2/token'

        url = urljoin(self.host, endpoint)

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.key,
            'client_secret': self.secret
        }

        r = requests.post(url, data=data)

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason)

        if r.json()['token_type'] == 'Bearer':
            return r.json()['access_token']

        else:
            raise requests.exceptions.HTTPError('could not authenticate to the PetFinder API')

    def animal_types(self, types=None):
        r"""
        Returns data on an animal type, or types available from the PetFinder API. This data includes the
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
        json or pandas DataFrame

        Examples
        --------

        """

        if types is None:
            url = urljoin(self.host, 'types')

            r = requests.get(url, headers={
                'Authorization': 'Bearer ' + self.auth,
            })

            result = r.json()

        elif isinstance(types, str):
            if str.lower(types) not in self._available_types:
                raise ValueError('type must be one of "dog", "cat", "rabbit", "small-furry", "horse", '
                                 '"bird", "scales-fins-others", "barnyard"')
            else:
                url = urljoin(self.host, 'types/{type}'.format(type=types))

                r = requests.get(url, headers={
                    'Authorization': 'Bearer ' + self.auth,
                })

                result = r.json()

        elif isinstance(types, (tuple, list)):
            types_check = list(set(types).difference(self._available_types))

            if len(types_check) >= 1:
                unknown_types = ', '.join(types_check)

                raise ValueError('animal types {types} not available. Must be one of "dog", "cat", "rabbit", '
                                 '"small-furry", "horse", "bird", "scales-fins-others", "barnyard"'
                                 .format(types=unknown_types))

            else:
                types_collection = []

                for type in types:
                    url = urljoin(self.host, 'types/{type}'.format(type=type))

                    r = requests.get(url, headers={
                        'Authorization': 'Bearer ' + self.auth,
                    })

                    types_collection.append(r.json()['type'])

            result = {'types': types_collection}

        else:
            raise TypeError('types parameter must be either None, str, list or tuple')

        return result

    def breeds(self, types=None, return_df=False, raw_results=False):
        r"""
        Returns breed names of specified animal type or types.

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
        json or pandas DataFrame

        Examples
        --------

        """
        if types is None or isinstance(types, (list, tuple)):
            if types is None:
                types = self._available_types

            else:
                types_check = list(set(types).difference(self._available_types))

                if len(types_check) >= 1:
                    unknown_types = ', '.join(types_check)

                    raise ValueError('animal types {types} not available. Must be one of "dog", "cat", "rabbit", '
                                     '"small-furry", "horse", "bird", "scales-fins-others", "barnyard"'
                                     .format(types=unknown_types))

            breeds = []

            for t in types:
                url = urljoin(self.host, 'types/{type}/breeds'.format(type=t))

                r = requests.get(url, headers={
                    'Authorization': 'Bearer ' + self.auth,
                })

                breeds.append({t: r.json()})

            result = {'breeds': breeds}

        elif isinstance(types, str):
            if str.lower(types) not in self._available_types:
                raise ValueError('type must be one of "dog", "cat", "rabbit", "small-furry", "horse", '
                                 '"bird", "scales-fins-others", "barnyard"')

            url = urljoin(self.host, 'types/{type}/breeds'.format(type=types))

            r = requests.get(url, headers={
                'Authorization': 'Bearer ' + self.auth,
            })

            result = r.json()

        else:
            raise TypeError('types parameter must be either None, str, list or tuple')

        if return_df:
            raw_results = True

            df_results = pd.DataFrame()

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

    def animals(self, animal_id=None, type=None, breed=None, size=None, gender=None,
                age=None, color=None, coat=None, status=None, name=None,
                organization=None, location=None, distance=None, sort=None, page=1,
                limit=20, return_df=False):
        r"""

        Parameters
        ----------
        animal_id : optional
        type : optional
        breed: optional
        size: optional
        gender : optional
        age : optional
        color : optional
        coat : optional
        status : optional
        name : optional
        organization : optional
        location : optional
        distance : optional
        sort : optional
        page : default 1
        limit : default 20
        return_df : boolean, default False


        Raises
        ------
        
        Returns
        -------


        """
        pass

    def organization(self, organization_id=None, name=None, location=None, distance=None, state=None,
                     country=None, query=None, sort=None,
                     page=1, limit=20, return_df=False):
        r"""

        Parameters
        ----------
        organization_id : optional
        name : optional
        location : optional
        distance : optional
        state : optional
        country : optional
        query : optional
        sort : optional
        page : default 1
        limit : default 20
        return_df : boolean, default False

        Raises
        ------

        Returns
        -------

        """

    #TODO: Make breed_list call breeds internally and add a Deprecation Warning.
    def breed_list(self, animal, outputformat='json', return_df=False):
        r"""
        Method for calling the 'breed.list' method of the Petfinder API. Returns the available breeds
        for the selected animal.

        Parameters
        ----------
        animal : str
            Return breeds of animal. Must be one of 'barnyard', 'bird', 'cat', 'dog', 'horse',
            'reptile', or 'smallfurry'
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.
        return_df : boolean, default=False
            If True, coerces results returned from the Petfinder API into a pandas DataFrame.

        Returns
        -------
        json, str or pandas DataFrame
            The breeds of the animal. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

        """
        method = 'breed.list'
        url = urljoin(self.host, method)

        if return_df:
            args = parameters(key=self.key, animal=animal, outputformat='json')
            r = query(url, args, method=method)
            r = json_normalize(r['petfinder']['breeds']['breed'])
            r.rename(columns={'$t': animal + ' breeds'}, inplace=True)
        else:
            args = parameters(key=self.key, animal=animal, outputformat=outputformat)
            r = query(url, args, return_df=return_df, method=method)

        return r

    def pet_find(self, location, animal=None, breed=None, size=None, sex=None, age=None, offset=None,
                 count=None, output=None, pages=None, outputformat='json', return_df=False):
        r"""
        Returns a collection of pet records matching input parameters.

        Parameters
        ----------
        location: str
            ZIP/postal code, state, or city and state to perform the search.
        animal : str, optional
            Animal type to search for. Must be one of 'barnyard', 'bird', 'cat', 'dog', 'horse',
            'reptile', or 'smallfurry'.
        breed : str, optional
            Specifies the breed of the animal to search.
        size: str, optional
            Specifies the size of the animal/breed to search. Must be one of 'S' (small),
            'M' (medium), 'L' (large), 'XL' (extra-large).
        sex : str, optional
            Filters the search to the desired gender of the animal. Must be one of 'M' (male) or 'F' (female).
        age : str, optional
            Returns animals with specified age. Must be one of 'Baby', 'Young', 'Adult', 'Senior'.
        offset : int, optional
            Can be set to the value of :code:`lastOffset` returned from the previous call to retrieve the next
            set of results. The :code:`pages` parameter can also be used to pull a desired number of paged
            results.
        count : str or int, optional
            The number of records to return. Default is 25.
        pages : int, optional
            The number of pages of results to return. For example, if :code:`pages=4` with the default
             :code:`count` parameter (25), 100 results would be returned. The paged results are returned
             as a list, but can be returned as a pandas DataFrame by setting :code:`return_df=True`.
        output : str, optional
            Sets the amount of information returned in each record. 'basic' returns a simple record while
            'full' returns a complete record with description. Defaults to 'basic'.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.
        return_df : boolean, default=False
            If True, coerces results returned from the Petfinder API into a pandas DataFrame.

        Returns
        -------
        json, list of json, str or list of str, or pandas DataFrame
            Pet records matching the desired search parameters. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If the :code:`pages` parameter is set, the paged results are
            returned as a list. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

        """
        method = 'pet.find'
        url = urljoin(self.host, method)

        args = parameters(key=self.key, animal=animal, breed=breed, size=size, sex=sex, location=location, age=age,
                          output=output, outputformat=outputformat, offset=offset, count=count)

        if return_df and outputformat != 'json':
            args.update(format='json')

        r = query(url, args, pages=pages, return_df=return_df, method=method, count=count)

        return r

    def pet_get(self, pet_id, outputformat='json', return_df=False):
        r"""
        Returns a single record for a pet.

        Parameters
        ----------
        pet_id : str
            ID of the pet record to return.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.
        return_df : boolean, default=False
            If True, coerces results returned from the Petfinder API into a pandas DataFrame.

        Returns
        -------
        json, str or pandas DataFrame
            Matching record corresponding to input pet ID. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

        """
        method = 'pet.get'
        url = urljoin(self.host, method)

        args = parameters(key=self.key, outputformat=outputformat, id=pet_id)

        if return_df and outputformat != 'json':
            args.update(format='json')

        if isinstance(pet_id, (string_types, int)):
            return query(url, args, return_df=return_df, method=method)

        else:
            return self.pets_get(pet_id, outputformat=outputformat, return_df=return_df)

    def pets_get(self, pet_id, outputformat='json', return_df=False):
        r"""
        Convenience wrapper of :code:`pet_get` for returning multiple pet records given a list or
        tuple of pet IDs.

        Parameters
        ----------
        pet_id : list or tuple
            List or tuple containing the pet IDs to search.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.
        return_df : boolean, default=False
            If True, coerces results returned from the Petfinder API into a pandas DataFrame.

        Returns
        -------
        list or pandas DataFrame
            Matching record corresponding to input pet ID. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

        See Also
        --------
        pet_get : Wrapped function called by :code:`pets_get`.

        """
        method = 'pet.get'
        url = urljoin(self.host, method)

        args = parameters(key=self.key, outputformat=outputformat)

        if return_df:
            args.update(outputformat='json')

        if isinstance(pet_id, (list, tuple)):
            return return_multiple_get_calls(call_id=pet_id, url=url, args=args, return_df=return_df, method=method)

        else:

            return self.pet_get(pet_id, outputformat=outputformat, return_df=return_df)

    def shelter_find(self, location, name=None, offset=None, count=None, pages=None,
                     return_df=False, outputformat='json'):
        r"""
        Returns a collection of shelter records matching input parameters.

        Parameters
        ----------
        location: str
            ZIP/postal code, state, or city and state to perform the search.
        name : str, optional (:code:`location` must be specified)
            Full or partial shelter name
        offset : int, optional
            Can be set to the value of :code:`lastOffset` returned from the previous call to retrieve the next
            set of results. The :code:`pages` parameter can also be used to pull a desired number of paged
            results.
        count : str or int, optional
            The number of records to return. Default is 25.
        pages : int, optional
            The number of pages of results to return. For example, if :code:`pages=4` with the default
             :code:`count` parameter (25), 100 results would be returned. The paged results are returned
             as a list.
        output : str, optional
            Sets the amount of information returned in each record. 'basic' returns a simple record while
            'full' returns a complete record with description. Defaults to 'basic'.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.
        return_df : boolean, default=False
            If True, coerces results returned from the Petfinder API into a pandas DataFrame.

        Returns
        -------
        json, list of json, str, list of str or pandas DataFrame
            Shelters matching specified input parameters. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If the :code:`pages` parameter is set, the paged results are
            returned as a list. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

        """
        method = 'shelter.find'
        url = urljoin(self.host, method)

        args = parameters(key=self.key, location=location, name=name, outputformat=outputformat, offset=offset,
                          count=count)

        if return_df and outputformat != 'json':
            args.update(format='json')

        return query(url, args, pages=pages, return_df=return_df, method=method, count=count)

    def shelter_get(self, shelter_id, return_df=False, outputformat='json'):
        r"""
        Returns a single shelter record.

        Parameters
        ----------
        shelter_id : str
            Desired shelter's ID
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.
        return_df : boolean, default=False
            If True, coerces results returned from the Petfinder API into a pandas DataFrame.

        Returns
        -------
        json, str or pandas DataFrame
            Shelter record of input shelter ID. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

        """
        method = 'shelter.get'
        url = urljoin(self.host, method)

        args = parameters(key=self.key, outputformat=outputformat, id=shelter_id)

        if return_df and outputformat != 'json':
            args.update(format='json')

        if isinstance(shelter_id, (string_types, int)):
            return query(url, args, return_df=return_df, method=method)

        else:

            return self.shelters_get(shelter_id, return_df=return_df, outputformat=outputformat)

    def shelters_get(self, shelter_id, return_df=False, outputformat='json'):
        r"""
        Returns multiple shelter records given a list or tuple of shelter IDs. Convenience wrapper function
        of :code:`shelter_get()`.

        Parameters
        ----------
        shelter_id : list or tuple
            List or tuple containing the shelter IDs to search.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.
        return_df : boolean, default=False
            If True, coerces results returned from the Petfinder API into a pandas DataFrame.

        Returns
        -------
        list or pandas DataFrame
            Shelter record of input shelter ID. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

        See Also
        --------
        shelter_get

        """
        method = 'shelter.get'
        url = urljoin(self.host, method)

        args = parameters(key=self.key, outputformat=outputformat, id=shelter_id)

        if return_df and outputformat != 'json':
            args.update(format='json')

        if isinstance(shelter_id, (list, tuple)):
            return return_multiple_get_calls(call_id=shelter_id, url=url, args=args,
                                             return_df=return_df, method=method)

        else:

            return self.shelter_get(shelter_id, return_df=return_df, outputformat=outputformat)

    def shelter_get_pets(self, shelter_id, status=None, offset=None, count=None, output=None, pages=None,
                         outputformat='json', return_df=False):
        r"""
        Returns a collection of pet records for an individual shelter.

        Parameters
        ----------
        shelter_id : str
            Desired shelter's ID
        status : str, optional
            Filters returned collection of pet records by the pet's status. Must be one of 'A' (adoptable, default),
            'H' (hold), 'P' (pending), 'X' (adopted/removed).
        offset : int, optional
            Can be set to the value of :code:`lastOffset` returned from the previous call to retrieve the next
            set of results. The :code:`pages` parameter can also be used to pull a desired number of paged
            results.
        count : str or int, optional
            The number of records to return. Default is 25.
        pages : int, optional
            The number of pages of results to return. For example, if :code:`pages=4` with the default
             :code:`count` parameter (25), 100 results would be returned. The paged results are returned
             as a list.
        output : str, optional
            Sets the amount of information returned in each record. 'basic' returns a simple record while
            'full' returns a complete record with description. Defaults to 'basic'.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.
        return_df : boolean, default=False
            If True, coerces results returned from the Petfinder API into a pandas DataFrame.

        Returns
        -------
        json, list of json, str, list of str, or pandas DataFrame
            Pet records of given shelter matching optional input parameters. If the parameter
            :code:`outputformat` is 'json', the result is formatted as a JSON object. Otherwise, the return
            object is a text representation of an XML object. If the :code:`pages` parameter is set, the
            paged results are returned as a list. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

        """
        method = 'shelter.getPets'
        url = urljoin(self.host, method)

        args = parameters(key=self.key, status=status, output=output, outputformat=outputformat, offset=offset,
                          count=count, id=shelter_id)

        if return_df and outputformat != 'json':
            args.update(format='json')

        return query(url, args, pages=pages, return_df=return_df, method=method, count=count)

    def shelter_list_by_breed(self, animal, breed, offset=None, count=None, pages=None,
                              outputformat='json', return_df=False):
        r"""
        Returns a list of shelter IDs listing animals matching the input animal breed.

        Parameters
        ---------
        animal : str
            Animal type to search for. Must be one of 'barnyard', 'bird', 'cat', 'dog', 'horse',
            'reptile', or 'smallfurry'.
        breed : str
            Specifies the breed of the animal to search.
        offset : int, optional
            Can be set to the value of :code:`lastOffset` returned from the previous call to retrieve the next
            set of results. The :code:`pages` parameter can also be used to pull a desired number of paged
            results.
        count : str or int, optional
            The number of records to return. Default is 25.
        pages : int, optional
            The number of pages of results to return. For example, if :code:`pages=4` with the default
            :code:`count` parameter (25), 100 results would be returned. The paged results are returned
            as a list.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.
        return_df : boolean, default=False
            If True, coerces results returned from the Petfinder API into a pandas DataFrame.

        Returns
        -------
        json, list of json, str, list of str or pandas DataFrame
            Shelter IDs listing animals matching the input animal breed. If the parameter
            :code:`outputformat` is 'json', the result is formatted as a JSON object. Otherwise, the
            return object is a text representation of an XML object. If the :code:`pages` parameter
            is set, the paged results are returned as a list. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

        """
        method = 'shelter.listByBreed'
        url = urljoin(self.host, method)

        args = parameters(key=self.key, animal=animal, breed=breed, outputformat=outputformat, offset=offset,
                          count=count)

        if return_df and outputformat != 'json':
            args.update(format='json')

        return query(url, args, pages=pages, return_df=return_df, method=method, count=count)
