import requests
from six.moves.urllib.parse import urljoin
import xml.etree.ElementTree as ET


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
    shelter_getPets(shelterId, status=None, offset=None, count=None, output=None, outputformat='json')
        Outputs a collection of pet IDs or records for the shelter specified by :code:`shelterID`
    shelter_listByBreed(animal, breed, offset=None, count=None, outputformat='json')
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

    def breed_list(self, animal, outputformat='json'):
        r"""
        Method for calling the 'breed.list' method of the Petfinder API. Returns the available breeds
        for the selected animal.

        Parameters
        ----------
        animal : str
            Return breeds of animal. Must be one of 'barnyard', 'bird', 'cat', 'dog', 'horse',
            'reptile', or 'smallfurry'
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'

        Returns
        -------
        json or str
            The breeds of the animal. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object.

        """
        url = urljoin(self.host, 'breed.list')

        args = _parameters(key=self.key, animal=animal, outputformat=outputformat)

        return _output(url, args)

    def pet_find(self, location, animal=None, breed=None, size=None, sex=None, age=None, offset=None,
                 count=None, output=None, pages=None, outputformat='json'):
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
             as a list.
        output : str, optional
            Sets the amount of information returned in each record. 'basic' returns a simple record while
            'full' returns a complete record with description. Defaults to 'basic'.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'

        Returns
        -------
        json, list of json, str or list of str
            Pet records matching the desired search parameters. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If the :code:`pages` parameter is set, the paged results are
            returned as a list.

        """
        url = urljoin(self.host, 'pet.find')

        args = _parameters(key=self.key, animal=animal, breed=breed, size=size, sex=sex, location=location,
                           age=age, offset=offset, count=count, output=output, outputformat=outputformat)

        return _output(url, args, pages = pages)

    def pet_get(self, petId, outputformat='json'):
        r"""
        Returns a single record for a pet.

        Parameters
        ----------
        petId : str
            ID of the pet record to return.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'.

        Returns
        -------
        json or str
            Matching record corresponding to input pet ID. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object.

        """
        url = urljoin(self.host, 'pet.get')

        args = _parameters(key=self.key, id=petId, outputformat=outputformat)

        return _output(url, args)

    def pet_getRandom(self, animal=None, breed=None, size=None,
                      sex=None, location=None, shelterId=None, output=None, outputformat='json'):
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
        shelterId : str, optional
            Filters randomly returned result down to a specific shelter.
        output : str, optional
            Sets the amount of information returned in each record. 'basic' returns a simple record while
            'full' returns a complete record with description. Defaults to 'basic'.
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'

        Returns
        -------
        json or str
            Randomly selected pet record. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object.

        """
        url = urljoin(self.host, 'pet.getRandom')

        args = _parameters(key=self.key, animal=animal, breed=breed, size=size, sex=sex,
                           location=location, shelterId=shelterId, output=output, outputformat=outputformat)

        return _output(url, args)

    def shelter_find(self, location, name=None, offset=None, count=None, pages=None, outputformat='json'):
        r"""
        Returns a collection of shelter records matching input parameters

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
            Output type of results. Must be one of 'json' (default) or 'xml'

        Returns
        -------
        json, list of json, str or list of str
            Shelters matching specified input parameters. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If the :code:`pages` parameter is set, the paged results are
            returned as a list.

        """
        url = urljoin(self.host, 'shelter.find')

        args = _parameters(key=self.key, location=location, offset=offset,
                           name=name, count=count, outputformat=outputformat)

        return _output(url, args, pages=pages)

    def shelter_get(self, shelterId, outputformat='json'):
        r"""
        Returns a single shelter record

        Parameters
        ----------
        shelterId : str
            Desired shelter's ID
        outputformat : str, default='json'
            Output type of results. Must be one of 'json' (default) or 'xml'

        Returns
        -------
        json or str
            Shelter record of input shelter ID. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object.

        """
        url = urljoin(self.host, 'shelter.get')

        args = _parameters(key=self.key, id=shelterId, outputformat=outputformat)

        return _output(url, args)

    def shelter_getPets(self, shelterId, status=None, offset=None, count=None, output=None,
                        pages=None, outputformat='json'):
        r"""
        Returns a collection of pet records for an individual shelter.

        Parameters
        ----------
        shelterId : str
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
            Output type of results. Must be one of 'json' (default) or 'xml'

        Returns
        -------
        json, list of json, str or list of str
            Pet records of given shelter matching optional input parameters. If the parameter
            :code:`outputformat` is 'json', the result is formatted as a JSON object. Otherwise, the return
            object is a text representation of an XML object. If the :code:`pages` parameter is set, the
            paged results are returned as a list.

        """
        url = urljoin(self.host, 'shelter.getPets')

        args = _parameters(key=self.key, id=shelterId, status=status, offset=offset, count=count,
                           output=output, outputformat=outputformat)

        return _output(url, args, pages=pages)

    def shelter_listByBreed(self, animal, breed, offset=None, count=None, pages=None, outputformat='json'):
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
            Output type of results. Must be one of 'json' (default) or 'xml'

        Returns
        -------
        json, list of json, str or list of str
            Shelter IDs listing animals matching the input animal breed. If the parameter
            :code:`outputformat` is 'json', the result is formatted as a JSON object. Otherwise, the
            return object is a text representation of an XML object. If the :code:`pages` parameter
            is set, the paged results are returned as a list.

        """
        url = urljoin(self.host, 'shelter.listByBreed')

        args = _parameters(key=self.key, animal=animal, breed=breed, offset=offset, count=count,
                           outputformat=outputformat)

        return _output(url, args, pages=pages)


def _parameters(key,
                animal=None,  # ('barnyard','bird', 'cat', 'dog', 'horse', 'reptile', 'smallfurry'),
                breed=None,
                size=None,  # ('S', 'M', 'L', 'XL'),
                sex=None,  # ('M', 'F'),
                location=None,
                name=None, # Name of shelter
                age=None, # ('Baby', 'Young', 'Adult', 'Senior')
                petId=None,
                shelterId=None,
                status=None, # (A=Adoptable, H=Hold, P=Pending, X=Adopted/Removed)
                output=None,  # 'basic',
                outputformat='json',
                offset=None,
                count=None,
                id=None):

    args = {
        'key': key,
        'animal': animal,
        'breed': breed,
        'size': size,
        'sex': sex,
        'age': age,
        'location': location,
        'name': name,
        'petId': petId,
        'shelterId': shelterId,
        'status': status,
        'output': output,
        'format': outputformat,
        'offset': offset,
        'count': count,
        'id': id
    }

    args = {key: val for key, val in args.items() if val is not None}

    return args


def _output(url, args, pages=None):

    r = requests.get(url, args)
    outputformat = args['format']

    if outputformat is 'json':
        r = r.json()
    else:
        r = r.text

    if pages is None:

        return r

    else:
        result = [r]
        outputformat = args['format']

        if outputformat is 'json':
            lastoffset = r['petfinder']['lastOffset']['$t']
        else:
            lastoffset = ET.fromstring(r.encode('utf-8'))[1].text

        try:
            count = args['count']
        except KeyError:
            count = 25

        for i in range(0, pages):

            args.update(offset=lastoffset)
            r = requests.get(url, args)

            if outputformat is 'json':
                result.append(r.json())
                lastoffset = r.json()['petfinder']['lastOffset']['$t']

            else:
                result.append(r.text)
                lastoffset = ET.fromstring(r.text.encode('utf-8'))[1].text

            if int(lastoffset) + count >= 2000:
                print('Next result set would exceed maximum 2,000 records per search, '
                      'returning results up to page ' + str(pages - 1))

                return result

        return result
