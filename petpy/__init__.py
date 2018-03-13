"""
Petpy Petfinder API library
"""

from xml.etree import ElementTree as ET

import requests
from numpy import nan
from pandas import DataFrame, concat
from pandas.io.json import json_normalize
from six.moves.urllib.parse import urljoin
from six import string_types


class Petfinder(object):
    r"""
    Wrapper class for the PetFinder API.

    Attributes
    ----------
    key : str
        The API key.
    secret: str, optional
        The secret key.

    Methods
    -------
    breed_list(animal, outputformat='json')
        Returns the breeds of :code:`animal`
    pet_find(location=None, animal=None, breed=None, size=None, sex=None, age=None, offset=None, count=None, output=None, outputformat='json')
        Returns a collection of pet records matching input parameters.
    pet_get(petId, outputformat='json')
        Returns a single pet record for the given :code:`petId`
    pet_getRandom(animal=None, breed=None, size=None, sex=None, location=None, shelterId=None, output=None, outputformat='json')
        Returns a randomly selected pet record. The optional parameters filter the records based on the specified characteristics
    shelter_find(location, name=None, offset=None, count=None, outputformat='json')
        Gets a collection of shelter records matching input parameters.
    shelter_get(shelterId, outputformat='json')
        Gets the record for the given :code:`shelterID`
    shelter_get_pets(shelterId, status=None, offset=None, count=None, output=None, outputformat='json')
        Outputs a collection of pet IDs or records for the shelter specified by :code:`shelterID`
    shelter_list_by_breed(animal, breed, offset=None, count=None, outputformat='json')
        Returns shelterIDs listing animals of the specified :code:`breed`

    """
    def __init__(self, key, secret=None):
        r"""

        Parameters
        ----------
        key : str
            API key given after `registering on the PetFinder site <https://www.petfinder.com/developers/api-key>`_
        secret : str, optional
            Secret API key given in addition to general API key. Only needed for requests that require
            authentication.

        """
        self.key = key
        self.secret = secret
        self.host = 'http://api.petfinder.com/'

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
            args = _parameters(key=self.key, animal=animal, outputformat='json')
            r = _query(url, args, method=method)
            r = json_normalize(r['petfinder']['breeds']['breed'])
            r.rename(columns={'$t': animal + ' breeds'}, inplace=True)
        else:
            args = _parameters(key=self.key, animal=animal, outputformat=outputformat)
            r = _query(url, args, return_df=return_df, method=method)

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

        args = _parameters(key=self.key, animal=animal, breed=breed, size=size, sex=sex, location=location, age=age,
                           output=output, outputformat=outputformat, offset=offset, count=count)

        if return_df and outputformat != 'json':
            args.update(format='json')

        r = _query(url, args, pages=pages, return_df=return_df, method=method, count=count)

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

        args = _parameters(key=self.key, outputformat=outputformat, id=pet_id)

        if return_df and outputformat != 'json':
            args.update(format='json')

        if isinstance(pet_id, (string_types, int)):
            return _query(url, args, return_df=return_df, method=method)

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

        args = _parameters(key=self.key, outputformat=outputformat)

        if return_df:
            args.update(outputformat='json')

        if isinstance(pet_id, (list, tuple)):
            return _return_multiple_get_calls(call_id=pet_id, url=url, args=args, return_df=return_df, method=method)

        else:

            return self.pet_get(pet_id, outputformat=outputformat, return_df=return_df)

    def pet_get_random(self, animal=None, breed=None, size=None, sex=None, location=None, shelter_id=None, output=None,
                       records=None, return_df=False, outputformat='json'):
        r"""
        Returns a randomly selected pet record. The possible result can be filtered with input parameters.

        Parameters
        ----------
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
        location: str, optional
            ZIP/postal code, state, or city and state to perform the search.
        shelter_id : str, optional
            Filters randomly returned result down to a specific shelter.
        output : str, optional
            Sets the amount of information returned in each record. 'basic' returns a simple record while
            'full' returns a complete record with description. Defaults to 'basic'.
        records : int, optional
            Returns :code:`records` random results. Each returned record is counted as one call to the
            Petfinder API.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.
        return_df : boolean, default=False
            If True, coerces results returned from the Petfinder API into a pandas DataFrame. If
            :code:`output` is not 'basic' or 'full', return_df is overridden to False as the API
            returns a simplified JSON object containing only a randomly selected petId.

        Returns
        -------
        json, str, list, or pandas DataFrame
            Randomly selected pet record. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If :code:`records` is specified, a list of the results
            is returned. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

        """
        method = 'pet.getRandom'
        url = urljoin(self.host, method)

        if return_df and output not in ('basic', 'full'):
            output = 'full'

        args = _parameters(key=self.key, animal=animal, breed=breed, size=size, sex=sex, location=location,
                           shelter_id=shelter_id, output=output, outputformat=outputformat)

        if records is not None:
            results = []
            for _ in range(0, records):
                results.append(_query(url, args, return_df=return_df, method=method))

            if return_df:
                results = concat(results)

            return results

        else:

            return _query(url, args, return_df=return_df, method=method)

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

        args = _parameters(key=self.key, location=location, name=name, outputformat=outputformat, offset=offset,
                           count=count)

        if return_df and outputformat != 'json':
            args.update(format='json')

        return _query(url, args, pages=pages, return_df=return_df, method=method, count=count)

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

        args = _parameters(key=self.key, outputformat=outputformat, id=shelter_id)

        if return_df and outputformat != 'json':
            args.update(format='json')

        if isinstance(shelter_id, (string_types, int)):
            return _query(url, args, return_df=return_df, method=method)

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

        args = _parameters(key=self.key, outputformat=outputformat, id=shelter_id)

        if return_df and outputformat != 'json':
            args.update(format='json')

        if isinstance(shelter_id, (list, tuple)):
            return _return_multiple_get_calls(call_id=shelter_id, url=url, args=args,
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

        args = _parameters(key=self.key, status=status, output=output, outputformat=outputformat, offset=offset,
                           count=count, id=shelter_id)

        if return_df and outputformat != 'json':
            args.update(format='json')

        return _query(url, args, pages=pages, return_df=return_df, method=method, count=count)

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

        args = _parameters(key=self.key, animal=animal, breed=breed, outputformat=outputformat, offset=offset,
                           count=count)

        if return_df and outputformat != 'json':
            args.update(format='json')

        return _query(url, args, pages=pages, return_df=return_df, method=method, count=count)


def _coerce_to_dataframe(x, method):

    if 'pet' in method or 'Pet' in method:

        res = media_df = opt_df = breed_df = DataFrame()

        if method == 'pet.get' or method == 'pet.getRandom':
            res, breed_df, opt_df, media_df = _pet_find_get_coerce(x['petfinder']['pet'])

        elif method == 'pet.find' or method == 'shelter.getPets':
            res = media_df = opt_df = breed_df = DataFrame()

            if x['petfinder']['pets'] == {}:
                return DataFrame()

            else:

                if isinstance(x['petfinder']['pets']['pet'], list):

                    for i in x['petfinder']['pets']['pet']:
                        pet, breed, opt, media = _pet_find_get_coerce(i)

                        res = res.append(pet)
                        breed_df = breed_df.append(breed)
                        opt_df = opt_df.append(opt)
                        media_df = media_df.append(media)

                else:
                    res, breed_df, opt_df, media_df = _pet_find_get_coerce(x['petfinder']['pets']['pet'])

        breed_df.columns = ['breed' + str(col) for col in breed_df.columns]
        opt_df.columns = ['status' + str(col) for col in opt_df.columns]
        media_df.columns = ['photos' + str(col) for col in media_df.columns]

        df = concat([res, breed_df, opt_df, media_df], axis=1)

        try:
            del df['breeds.breed']
            del df['breeds.breed.$t']
            del df['breeds.breed']
            del df['media.photos.photo']
        except KeyError:
            pass

    else:

        if method == 'shelter.find' or method == 'shelter.listByBreed':
            try:
                df = json_normalize(x['petfinder']['shelters']['shelter'])
            except (KeyError, ValueError):
                print('No shelters matching criteria found')
                raise

        elif method == 'shelter.get':
            try:
                df = json_normalize(x['petfinder']['shelter'])

            except (KeyError, ValueError):
                df = DataFrame({'shelterId': 'shelter opt-out'}, index=[0])

        else:
            raise ValueError('unknown API method')

    df.columns = [col.replace('.$t', '') for col in df.columns]
    df.columns = [col.replace('contact.', '') for col in df.columns]

    df = df[df.columns[~df.columns.str.contains('options')]]

    return df


def _pet_find_get_coerce(x):
    res = media_df = opt_df = breed_df = DataFrame()

    try:
        breed = DataFrame(json_normalize(x['breeds']['breed'])['$t'].to_dict(), index=[0])
    except (KeyError, TypeError):
        breed = DataFrame([nan], columns=[0])

    try:
        media = DataFrame(json_normalize(x['media']['photos']['photo'])['$t'].to_dict(), index=[0])
    except (KeyError, TypeError):
        media = DataFrame([nan], columns=[0])

    try:
        options = DataFrame(json_normalize(x['options']['option'])['$t'].to_dict(), index=[0])
    except (KeyError, TypeError):
        options = DataFrame([nan], columns=[0])

    breed_df = breed_df.append(breed)
    opt_df = opt_df.append(options)
    media_df = media_df.append(media)
    res = res.append(json_normalize(x))

    return res, breed_df, opt_df, media_df


def _parameters(key, animal=None, breed=None, size=None, sex=None, location=None, name=None, age=None, pet_id=None,
                shelter_id=None, status=None, output=None, outputformat='json', offset=None, count=None, id=None):

    args = {
        'key': key,
        'animal': animal,
        'breed': breed,
        'size': size,
        'sex': sex,
        'age': age,
        'location': location,
        'name': name,
        'petId': pet_id,
        'shelterId': shelter_id,
        'status': status,
        'output': output,
        'format': outputformat,
        'offset': offset,
        'count': count,
        'id': id
    }

    args = {key: val for key, val in args.items() if val is not None}

    return args


def _query(url, args, pages=None, return_df=False, method=None, count=None):

    if return_df:
        args.update(format='json')
        outputformat = 'json'
    else:
        outputformat = args['format']

    r = requests.get(url, args)

    if outputformat is 'json':
        r = r.json()
    else:
        r = r.text

    if pages is None:

        if return_df is False:
            return r
        else:
            r = _coerce_to_dataframe(r, method)

            return r

    else:

        if return_df:
            result = [_coerce_to_dataframe(r, method)]
        else:
            result = [r]

        try:
            if outputformat is 'json':
                lastoffset = r['petfinder']['lastOffset']['$t']
            else:
                lastoffset = ET.fromstring(r.encode('utf-8'))[1].text

        except KeyError:
            return result[0]

        if pages > 1:
            pages = pages - 1

        for _ in range(0, pages):

            args.update(offset=lastoffset)
            r = requests.get(url, args)

            if outputformat is 'json':
                if return_df:
                    result.append(_coerce_to_dataframe(r.json(), method))
                else:
                    result.append(r.json())

                try:
                    lastoffset = r.json()['petfinder']['lastOffset']['$t']

                    if int(lastoffset) == 1 and count != 1:
                        return result[0]

                except (KeyError, ValueError):
                    if return_df:
                        result = concat(result)

                    return result

            else:
                result.append(r.text)

                try:
                    lastoffset = ET.fromstring(r.text.encode('utf-8'))[1].text
                except (KeyError, ValueError):
                    if return_df:
                        result = concat(result)

                    return result

        if return_df:
            result = concat(result)

        return result


def _return_multiple_get_calls(call_id, url, args, return_df, method):
    responses = []

    for i in call_id:
        args.update(id=i)
        responses.append(_query(url, args, return_df=return_df, method=method))

    if return_df:
        return concat(responses, axis=0)

    return responses
