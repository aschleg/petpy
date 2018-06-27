# encoding=utf-8

from xml.etree import ElementTree as ET

import requests
from pandas import DataFrame, concat
from pandas.io.json import json_normalize


def coerce_to_dataframe(x, method):

    if 'pet' in method or 'Pet' in method:

        res = media_df = opt_df = breed_df = DataFrame()

        if method == 'pet.get' or method == 'pet.getRandom':
            res, breed_df, opt_df, media_df = pet_find_get_coerce(x['petfinder']['pet'])

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
                        pet, breed, opt, media = pet_find_get_coerce(i)

                        res = res.append(pet)
                        breed_df = breed_df.append(breed)
                        opt_df = opt_df.append(opt)
                        media_df = media_df.append(media)

                else:
                    res, breed_df, opt_df, media_df = pet_find_get_coerce(x['petfinder']['pets']['pet'])

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
                df = empty_shelter_df()

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


def pet_find_get_coerce(x):
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


def parameters(key, animal=None, breed=None, size=None, sex=None, location=None, name=None, age=None, pet_id=None,
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


def query(url, args, pages=None, return_df=False, method=None, count=None):
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
            r = coerce_to_dataframe(r, method)

            return r

    else:

        if return_df:
            result = [coerce_to_dataframe(r, method)]
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
                    result.append(coerce_to_dataframe(r.json(), method))
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


def return_multiple_get_calls(call_id, url, args, return_df, method):
    responses = []

    for i in call_id:
        args.update(id=i)
        responses.append(query(url, args, return_df=return_df, method=method))

    if return_df:
        return concat(responses, axis=0)

    return responses


def empty_shelter_df():
    return DataFrame(columns=['address1', 'address2', 'city', 'country', 'email', 'id', 'latitude',
                                 'longitude', 'name', 'phone', 'state', 'zip'])
