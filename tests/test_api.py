import os
import pytest
import vcr
import pandas as pd
from pandas import DataFrame

from petpy.api import Petfinder

tape = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    serializer='json',
    record_mode='once'
)


key = os.environ.get('PETFINDER_KEY')
secret_key = os.environ.get('PETFINDER_SECRET_KEY')


def authenticate():
    pf = Petfinder(key=key, secret=secret_key)

    return pf


pf = authenticate()


@vcr.use_cassette('tests/cassettes/authenticate.yml')
def test_authentication():
    p = Petfinder(key=key, secret=secret_key)

    assert isinstance(p.auth, str)


@vcr.use_cassette('tests/cassettes/animal_types.yml')
def test_animal_types():
    response1 = pf.animal_types()
    response2 = pf.animal_types('cat')
    response3 = pf.animal_types(['cat', 'dog'])

    assert isinstance(response1, dict)
    assert isinstance(response2, dict)
    assert str.lower(response2['type']['name']) == 'cat'

    assert isinstance(response3, dict)
    assert str.lower(response3['type'][0]['name']) == 'cat'
    assert str.lower(response3['type'][1]['name']) == 'dog'


@vcr.use_cassette('tests/cassettes/breeds.yml')
def test_breeds():

    animal_types = ('dog', 'cat', 'rabbit', 'small-furry',
                    'horse', 'bird', 'scales-fins-other', 'barnyard')

    response1 = pf.breeds()
    response1_df = pf.breeds(return_df=True)
    response2 = pf.breeds('cat')
    response2_df = pf.breeds('cat', return_df=True)
    response3 = pf.breeds(['cat', 'dog'])
    response3_df = pf.breeds(['cat', 'dog'], return_df=True)

    assert isinstance(response1, dict)
    assert len(list(set(list(response1['breeds'].keys())).difference(animal_types))) == 0
    assert isinstance(response1_df, DataFrame)

    assert isinstance(response2, dict)
    assert isinstance(response2['breeds']['cat'], list)
    assert isinstance(response2_df, DataFrame)

    assert isinstance(response3, dict)
    assert len(list(set(list(response3['breeds'].keys())).difference(animal_types))) == 0
    assert isinstance(response3_df, DataFrame)
