# encoding=utf-8


import pandas as pd
from pandas import concat, DataFrame
from pandas.io.json import json_normalize
import requests
from urllib.parse import urljoin


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

        self._animal_types = ('dog', 'cat', 'rabbit', 'small-furry',
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
            if str.lower(types) not in self._animal_types:
                raise ValueError('type must be one of "dog", "cat", "rabbit", "small-furry", "horse", '
                                 '"bird", "scales-fins-others", "barnyard"')
            else:
                url = urljoin(self.host, 'types/{type}'.format(type=types))

                r = requests.get(url,
                                 headers={
                                     'Authorization': 'Bearer ' + self.auth
                                 })

                result = r.json()

        elif isinstance(types, (tuple, list)):
            types_check = list(set(types).difference(self._animal_types))

            if len(types_check) >= 1:
                unknown_types = ', '.join(types_check)

                raise ValueError('animal types {types} not available. Must be one of "dog", "cat", "rabbit", '
                                 '"small-furry", "horse", "bird", "scales-fins-others", "barnyard"'
                                 .format(types=unknown_types))

            else:
                types_collection = []

                for type in types:
                    url = urljoin(self.host, 'types/{type}'.format(type=type))

                    r = requests.get(url,
                                     headers={
                                         'Authorization': 'Bearer ' + self.auth
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
                types = self._animal_types

            else:
                types_check = list(set(types).difference(self._animal_types))

                if len(types_check) >= 1:
                    unknown_types = ', '.join(types_check)

                    raise ValueError('animal types {types} not available. Must be one of "dog", "cat", "rabbit", '
                                     '"small-furry", "horse", "bird", "scales-fins-others", "barnyard"'
                                     .format(types=unknown_types))

            breeds = []

            for t in types:
                url = urljoin(self.host, 'types/{type}/breeds'.format(type=t))

                r = requests.get(url,
                                 headers={
                                     'Authorization': 'Bearer ' + self.auth
                                 })

                breeds.append({t: r.json()})

            result = {'breeds': breeds}

        elif isinstance(types, str):
            if str.lower(types) not in self._animal_types:
                raise ValueError('type must be one of "dog", "cat", "rabbit", "small-furry", "horse", '
                                 '"bird", "scales-fins-others", "barnyard"')

            url = urljoin(self.host, 'types/{type}/breeds'.format(type=types))

            r = requests.get(url,
                             headers={
                                 'Authorization': 'Bearer ' + self.auth
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

    def organizations(self, organization_id=None, name=None, location=None, distance=None, state=None,
                     country=None, query=None, sort=None, result_count=20, return_df=False):
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
        results_per_page : int, default 20
        return_df : boolean, default False

        Raises
        ------

        Returns
        -------

        """
        if organization_id is not None:

            url = urljoin(self.host, 'organizations/{id}')

            if isinstance(organization_id, (tuple, list)):

                organizations = []

                for org_id in organization_id:
                    r = requests.get(url.format(id=org_id),
                                     headers={
                                         'Authorization': 'Bearer ' + self.auth
                                     })

                    organizations.append(r.json())

            else:
                r = requests.get(url.format(id=organization_id),
                                 headers={
                                     'Authorization': 'Bearer ' + self.auth
                                 })

                organizations = r.json()

        else:
            url = urljoin(self.host, 'organizations/')

            params = _parameters(name=name, location=location, distance=distance,
                                 state=state, country=country, query=query, sort=sort,
                                 results_per_page=results_per_page, page=page)

            r = requests.get(url,
                             headers={
                                 'Authorization': 'Bearer ' + self.auth
                             },
                             params=params)

            organizations = r.json()

        return organizations


def _parameters(animal=None, breed=None, size=None, sex=None, location=None, distance=None, state=None,
                country=None, query=None, sort=None, name=None, age=None, animal_id=None, organization_id=None,
                status=None, page=None, results_per_page=None):

    args = {
        'animal': animal,
        'breed': breed,
        'size': size,
        'sex': sex,
        'age': age,
        'location': location,
        'distance': distance,
        'state': state,
        'country': country,
        'query': query,
        'sort': sort,
        'name': name,
        'animal_id': animal_id,
        'organization_id': organization_id,
        'status': status,
        'page': page,
        'limit': results_per_page
    }

    args = {key: val for key, val in args.items() if val is not None}

    return args


def _coerce_to_dataframe(x, method):

    if 'pet' in method or 'Pet' in method:

        res = media_df = opt_df = breed_df = DataFrame()

        if method == 'pet.get' or method == 'pet.getRandom':
            res, breed_df, opt_df, media_df = _pet_find_get_coerce(x['petfinder']['pet'])

        elif method == 'pet.find' or method == 'shelter.getPets':
            res = media_df = opt_df = breed_df = DataFrame()

            try:
                if x['petfinder']['pets'] == {}:
                    return DataFrame()
            except KeyError:
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
                df = _empty_shelter_df()

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
        breed = DataFrame(['na'], columns=[0])

    try:
        media = DataFrame(json_normalize(x['media']['photos']['photo'])['$t'].to_dict(), index=[0])
    except (KeyError, TypeError):
        media = DataFrame(['na'], columns=[0])

    try:
        options = DataFrame(json_normalize(x['options']['option'])['$t'].to_dict(), index=[0])
    except (KeyError, TypeError):
        options = DataFrame(['na'], columns=[0])

    breed_df = breed_df.append(breed)
    opt_df = opt_df.append(options)
    media_df = media_df.append(media)
    res = res.append(json_normalize(x))

    return res, breed_df, opt_df, media_df


def _return_multiple_get_calls(call_id, url, args, return_df, method):
    responses = []

    for i in call_id:
        args.update(id=i)
        responses.append(_query(url, args, return_df=return_df, method=method))

    if return_df:
        return concat(responses, axis=0)

    return responses


def _empty_shelter_df():
    return DataFrame(columns=['address1', 'address2', 'city', 'country', 'email', 'id', 'latitude',
                                 'longitude', 'name', 'phone', 'state', 'zip'])


def _query(url, args, pages=None, return_df=False, method=None, count=None):
    # Check value of count parameter to make sure it is not above 1000
    if count is not None:

        if not isinstance(count, int):
            try:
                count = int(count)
            except (TypeError, ValueError):
                raise ValueError('count parameter must be an integer or coercible to an integer.')

        if count > 1000:
            raise ValueError('count parameter cannot exceed 1,000. Please try using a combination of the pages and '
                             'count parameter to extract more than 1,000 records for a single call.')

    if pages is not None:

        if not isinstance(pages, int):
            try:
                pages = int(pages)
            except (TypeError, ValueError):
                raise ValueError('pages parameter must be an integer or coercible to an integer.')

        if count is not None:
            if pages * count > 2000:
                raise ValueError('A single API call cannot exceed more than 2,000 records.')

    if return_df:
        args.update(format='json')
        outputformat = 'json'
    else:
        outputformat = args['format']

    r = requests.get(url, args)

    # Check that call hasn't exceeded API daily limit

    if r.text.find('exceeded daily request limit') != -1 or r.status_code == 202:
        raise ValueError('Daily API limit exceeded')

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
