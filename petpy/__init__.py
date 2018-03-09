"""
Petpy Petfinder API library
"""
from xml.etree import ElementTree as ET

import requests
from numpy import nan
from pandas import DataFrame, concat
from pandas.io.json import json_normalize

from petpy.api import Petfinder


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
                for i in x['petfinder']['pets']['pet']:
                    pet, breed, opt, media = _pet_find_get_coerce(i)

                    res = res.append(pet)
                    breed_df = breed_df.append(breed)
                    opt_df = opt_df.append(opt)
                    media_df = media_df.append(media)

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
            df = json_normalize(x['petfinder']['shelters']['shelter'])
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


def _query(url, args, pages=None, return_df=False, method=None, count=None):

    if return_df == True:
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

        if return_df == False:
            return r
        else:
            r = _coerce_to_dataframe(r, method)

            return r

    else:

        if return_df == True:
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
                if return_df == True:
                    result.append(_coerce_to_dataframe(r.json(), method))
                else:
                    result.append(r.json())

                try:
                    lastoffset = r.json()['petfinder']['lastOffset']['$t']

                    if int(lastoffset) == 1 and count != 1:
                        return result[0]

                except (KeyError, ValueError):
                    if return_df == True:
                        result = concat(result)

                    return result

            else:
                result.append(r.text)

                try:
                    lastoffset = ET.fromstring(r.text.encode('utf-8'))[1].text
                except (KeyError, ValueError):
                    if return_df == True:
                        result = concat(result)

                    return result

        if return_df == True:
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