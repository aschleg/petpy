import os
import json
import xml.etree.ElementTree as ET
import pytest
import vcr
from six import string_types

from petpy import Petfinder


tape = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    serializer='json',
    # Either use existing cassettes, or never use recordings:
    record_mode='once'
)


#key = os.environ.get('PETFINDER_KEY')

def authenticate():
    pf = Petfinder(str(key))

    return pf


pf = authenticate()


@pytest.fixture
def top_level_keys():
    return ['@encoding', '@version', 'petfinder', '@xmlns:xsi']


@pytest.fixture
def petfinder_keys():
    return ['@xmlns:xsi', 'lastOffset', 'breeds', 'shelters', 'petIds',
            'pets', 'header', '@xsi:noNamespaceSchemaLocation']


@pytest.fixture
def petfinder_pet_get_keys():
    return ['@encoding', '@version', 'petfinder', 'options', 'status', 'contact', 'age',
            'pet', '@xmlns:xsi', 'header', '@xsi:noNamespaceSchemaLocation', 'size', 'media',
            'id', 'shelterPetId', 'breeds', 'name', 'sex', 'description', 'mix', 'shelterId', 'lastUpdate', 'animal']


@pytest.fixture
def petfinder_shelter_get_keys():
    return ['country', 'longitude', 'name', 'phone', 'state', 'address2',
            'email', 'city', 'zip', 'fax', 'latitude', 'id', 'address1']


@vcr.use_cassette('tests/cassettes/breed_list.yml', filter_query_parameters=['key'])
def test_breed_list(top_level_keys, petfinder_keys):

    response1 = pf.breed_list('cat')
    response2 = pf.breed_list('dog', 'xml')
    r = ET.fromstring(response2.encode('utf-8'))

    assert isinstance(response1, dict)
    assert isinstance(response2, string_types)

    assert set(response1.keys()).issubset(top_level_keys)
    assert set(response1['petfinder'].keys()).issubset(petfinder_keys)

    assert str(r[1].attrib) == "{'animal': 'dog'}"
    assert r[0].tag == 'header'
    assert r[1].tag == 'breeds'


@vcr.use_cassette('tests/cassettes/pet_find.yml', filter_query_parameters=['key'])
def test_pet_find(top_level_keys, petfinder_keys):
    response1 = pf.pet_find(location='98133', count=1)
    response2 = pf.pet_find(location='98133', count=1, outputformat='xml')
    r = ET.fromstring(response2.encode('utf-8'))

    assert isinstance(response1, dict)
    assert isinstance(response2, string_types)

    assert set(response1.keys()).issubset(top_level_keys)
    assert set(response1['petfinder'].keys()).issubset(petfinder_keys)

    assert r[0].tag == 'header'
    assert r[2].tag == 'pets'
    assert r[2][0].tag == 'pet'


@vcr.use_cassette('tests/cassettes/pet_getRandom.yml', filter_query_parameters=['key'])
def test_pet_getRandom(top_level_keys, petfinder_keys):

    response1 = pf.pet_getRandom()
    response2 = pf.pet_getRandom(outputformat='xml')
    r = ET.fromstring(response2.encode('utf-8'))

    assert isinstance(response1, dict)
    assert isinstance(response2, string_types)

    assert set(response1.keys()).issubset(top_level_keys)
    assert set(response1['petfinder'].keys()).issubset(petfinder_keys)

    assert r[0].tag == 'header'
    assert r[1].tag == 'petIds'
    assert r[1][0].tag == 'id'


@vcr.use_cassette('tests/cassettes/pet_get.yml', filter_query_parameters=['key'])
def test_pet_get(top_level_keys, petfinder_pet_get_keys):
    # Call pet_getRandom to get a valid petId to ensure test is run correctly
    petid = pf.pet_getRandom()['petfinder']['petIds']['id']['$t']

    response1 = pf.pet_get(petid)
    response2 = pf.pet_get(petid, outputformat='xml')
    r = ET.fromstring(response2.encode('utf-8'))

    assert isinstance(response1, dict)
    assert isinstance(response2, string_types)

    assert set(response1.keys()).issubset(top_level_keys)
    assert set(response1['petfinder'].keys()).issubset(petfinder_pet_get_keys)
    assert set(response1['petfinder']['pet'].keys()).issubset(petfinder_pet_get_keys)

    assert r[0].tag == 'header'
    assert r[1].tag == 'pet'
    assert r[1][0].tag == 'id'
    assert r[1][1].tag == 'shelterId'
    assert r[1][2].tag == 'shelterPetId'


@vcr.use_cassette('tests/cassettes/shelter_find.yml', filter_query_parameters=['key'])
def test_shelter_find(top_level_keys, petfinder_keys):

    response1 = pf.shelter_find('98115')
    response2 = pf.shelter_find('98115', outputformat='xml')
    r = ET.fromstring(response2.encode('utf-8'))

    assert isinstance(response1, dict)
    assert isinstance(response2, string_types)

    assert set(response1.keys()).issubset(top_level_keys)
    assert set(response1['petfinder'].keys()).issubset(petfinder_keys)

    assert r[0].tag == 'header'
    assert r[1].tag == 'lastOffset'
    assert r[2].tag == 'shelters'


@vcr.use_cassette('tests/cassettes/shelter_get.yml', filter_query_parameters=['key'])
def test_shelter_get(top_level_keys, petfinder_shelter_get_keys):
    shelterid = pf.shelter_find('98133', count=1)['petfinder']['shelters']['shelter']['id']['$t']

    response1 = pf.shelter_get(shelterid)
    response2 = pf.shelter_get(shelterid, outputformat='xml')
    r = ET.fromstring(response2.encode('utf-8'))

    assert isinstance(response1, dict)
    assert isinstance(response2, string_types)

    assert set(response1.keys()).issubset(top_level_keys)
    assert set(response1['petfinder']['shelter'].keys()).issubset(petfinder_shelter_get_keys)

    assert r[0].tag == 'header'
    assert r[1].tag == 'shelter'
    assert r[1][0].tag == 'id'


@vcr.use_cassette('tests/cassettes/shelter_getPets.yml', filter_query_parameters=['key'])
def test_shelter_getPets(top_level_keys, petfinder_keys):
    shelterid = pf.shelter_find('98133', count=1)['petfinder']['shelters']['shelter']['id']['$t']

    response1 = pf.shelter_getPets(shelterid, count=1)
    response2 = pf.shelter_getPets(shelterid, count=1, outputformat='xml')
    r = ET.fromstring(response2.encode('utf-8'))

    assert isinstance(response1, dict)
    assert isinstance(response2, string_types)

    assert set(response1.keys()).issubset(top_level_keys)
    assert set(response1['petfinder'].keys()).issubset(petfinder_keys)

    assert r[0].tag == 'header'
    assert r[1].tag == 'lastOffset'
    assert r[2].tag == 'pets'


@vcr.use_cassette('tests/cassettes/shelter_listByBreed.yml', filter_query_parameters=['key'])
def test_shelter_listByBreed(top_level_keys, petfinder_keys):

    response1 = pf.shelter_listByBreed('cat', 'American Shorthair', count=1)
    response2 = pf.shelter_listByBreed('cat', 'American Shorthair', count=1, outputformat='xml')
    r = ET.fromstring(response2.encode('utf-8'))

    assert isinstance(response1, dict)
    assert isinstance(response2, string_types)

    assert set(response1.keys()).issubset(top_level_keys)
    assert set(response1['petfinder'].keys()).issubset(petfinder_keys)

    assert r[0].tag == 'header'
    assert r[1].tag == 'shelters'


def test_paging_results(top_level_keys):

    response1 = pf.pet_find(location='98133', pages=3)
    response2 = pf.pet_find(location='98133', pages=3, outputformat='xml')

    assert isinstance(response1, list)

    assert len(response1) == len(response2) == 4

    for i in response1:
        assert set(i.keys()).issubset(top_level_keys)

    for j in response2:
        r = ET.fromstring(j.encode('utf-8'))
        assert r[0].tag == 'header'
        assert r[1].tag == 'lastOffset'
