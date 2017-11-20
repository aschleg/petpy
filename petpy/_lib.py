from pandas import DataFrame, concat
from pandas.io.json import json_normalize
from numpy import nan
import requests
import xml.etree.ElementTree as ET


def _coerce_to_dataframe(x, method):

    if 'pet' in method:

        res = media_df = opt_df = breed_df = DataFrame()

        if method == 'pet.get' or method == 'pet.getRandom':
            res, breed_df, opt_df, media_df = _pet_find_get_coerce(x['petfinder']['pet'])

        elif method == 'pet.find':

            res = media_df = opt_df = breed_df = DataFrame()

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
        except KeyError:
            pass

    elif 'shelter' in method:

        if method == 'shelter.find' or method == 'shelter.listByBreed':
            df = json_normalize(x['petfinder']['shelters']['shelter'])
        elif method == 'shelter.get':
            df = json_normalize(x['petfinder']['shelter'])
        elif method == 'shelter.getPets':
            df = json_normalize(x['petfinder']['pets']['pet'])
        else:
            raise ValueError('unknown API method')

    df.columns = [col.replace('.$t', '') for col in df.columns]

    return df


def _pet_find_get_coerce(x):
    res = media_df = opt_df = breed_df = DataFrame()

    breed = DataFrame(json_normalize(x['breeds']['breed'])['$t'].to_dict(), index=[0])

    try:
        media = DataFrame(json_normalize(x['media']['photos']['photo'])['$t'].to_dict(), index=[0])

    except KeyError:
        media = DataFrame([nan], columns=[0])

    try:
        options = DataFrame(json_normalize(x['options']['option'])['$t'].to_dict(), index=[0])

    except KeyError:
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


def _query(url, args, pages=None, return_df=False, method=None):

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

        if outputformat is 'json':
            lastoffset = r['petfinder']['lastOffset']['$t']
        else:
            lastoffset = ET.fromstring(r.encode('utf-8'))[1].text

        try:
            count = args['count']
        except KeyError:
            count = 25

        for _ in range(0, pages):

            args.update(offset=lastoffset)
            r = requests.get(url, args)

            if outputformat is 'json':
                if return_df == True:
                    result.append(_coerce_to_dataframe(r.json(), method))
                else:
                    result.append(r.json())

                lastoffset = r.json()['petfinder']['lastOffset']['$t']

            else:
                result.append(r.text)
                lastoffset = ET.fromstring(r.text.encode('utf-8'))[1].text

            if int(lastoffset) + count >= 2000:
                print('Next result set would exceed maximum 2,000 records per search, '
                      'returning results up to page ' + str(pages - 1))

                return result

        if return_df == True:
            result = concat(result)

        return result
<<<<<<< HEAD


def _return_multiple_get_calls(call_id, url, args, return_df, method):
    responses = []

    for i in call_id:
        args.update(id=i)
        responses.append(_query(url, args, return_df=return_df, method=method))

    if return_df:
        return concat(responses, axis=0)

    return responses
=======
>>>>>>> parent of fb03829... commit latest
