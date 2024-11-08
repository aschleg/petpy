import os
import pytest
import vcr
import time

from pandas import DataFrame
from dotenv import load_dotenv
from petpy.api import Petfinder


tape = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    serializer='json',
    record_mode='all'
)

load_dotenv('.env')
key = os.environ.get('PETPY_PETFINDER_KEY')
secret_key = os.environ.get('PETPY_PETFINDER_SECRET_KEY')

animal_types = ('dog', 'cat', 'rabbit', 'small-furry',
                'horse', 'bird', 'scales-fins-other', 'barnyard')


@vcr.use_cassette('tests/cassettes/authenticate.yml')
def test_authentication():
    p = Petfinder(key=key, secret=secret_key)

    assert isinstance(p._access_token, str)


def authenticate():
    pf = Petfinder(key=key, secret=secret_key)
    return pf


pf = authenticate()


@vcr.use_cassette('tests/cassettes/animal_types.yml')
def test_animal_types():
    time.sleep(2)
    response1 = pf.animal_types()
    time.sleep(2)
    response2 = pf.animal_types('cat')
    time.sleep(2)
    response3 = pf.animal_types(['cat', 'dog'])

    assert isinstance(response1, dict)
    assert isinstance(response2, dict)
    assert str.lower(response2['type']['name']) == 'cat'

    assert isinstance(response3, dict)
    assert str.lower(response3['types'][0]['name']) == 'cat'
    assert str.lower(response3['types'][1]['name']) == 'dog'

    with pytest.raises(ValueError):
        time.sleep(2)
        pf.animal_types(types='elephant')
    with pytest.raises(ValueError):
        time.sleep(2)
        pf.animal_types(types=['dragon', 'unicorn'])
    with pytest.raises(TypeError):
        time.sleep(2)
        pf.animal_types(types={})


@vcr.use_cassette('tests/cassettes/breeds.yml')
def test_breeds():
    time.sleep(2)
    response1 = pf.breeds()
    time.sleep(2)
    response1_df = pf.breeds(return_df=True)
    time.sleep(2)
    response2 = pf.breeds('cat')
    time.sleep(2)
    response2_df = pf.breeds('cat', return_df=True)
    time.sleep(2)
    response3 = pf.breeds(['cat', 'dog'])
    time.sleep(2)
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

    with pytest.raises(ValueError):
        time.sleep(2)
        pf.breeds(types='elephant')
    with pytest.raises(ValueError):
        time.sleep(2)
        pf.breeds(types=['dragon', 'unicorn'])
    with pytest.raises(TypeError):
        time.sleep(2)
        pf.breeds(types={})


@vcr.use_cassette('tests/cassettes/animals.yml')
def test_animals():
    response1 = pf.animals()
    time.sleep(2)
    response1_df = pf.animals(return_df=True)
    time.sleep(2)
    response2 = pf.animals(results_per_page=50, pages=3)
    time.sleep(2)
    response2_df = pf.animals(results_per_page=50, pages=3, return_df=True)

    animal_ids = []
    for i in response1['animals'][0:3]:
        animal_ids.append(i['id'])
    time.sleep(2)
    response3 = pf.animals(animal_id=animal_ids, results_per_page=5)
    time.sleep(2)
    response3_df = pf.animals(animal_id=animal_ids, return_df=True, results_per_page=5)
    time.sleep(2)
    response4 = pf.animals(animal_id=animal_ids[0], results_per_page=5)
    time.sleep(2)
    response4_df = pf.animals(animal_id=animal_ids[0], return_df=True, results_per_page=5)
    time.sleep(2)
    response5 = pf.animals(good_with_children=1, good_with_cats=1, results_per_page=5)
    time.sleep(2)
    response6 = pf.animals(before_date='2020-06-30', after_date='2020-01-01', results_per_page=5)
    time.sleep(2)
    response7 = pf.animals(before_date='2020-06-30 0:0:0', after_date='2020-01-01 12:00:00', results_per_page=5)
    time.sleep(2)
    response8 = pf.animals(good_with_dogs=1, results_per_page=5)
    time.sleep(2)
    response9 = pf.animals(good_with_dogs=1, good_with_cats=1, good_with_children=1, return_df=True,
                           results_per_page=5)
    time.sleep(2)
    response10 = pf.animals(special_needs=1, house_trained=1, declawed=1, return_df=True, results_per_page=5)
    time.sleep(2)
    with pytest.raises(ValueError):
        pf.animals(after_date='2021-07-02', before_date='2021-07-01', results_per_page=5)
    time.sleep(2)
    response11 = pf.animals(status=['found', 'adoptable'], results_per_page=5)

    assert isinstance(response1, dict)
    assert len(response1['animals']) == 20
    assert isinstance(response1_df, DataFrame)

    assert isinstance(response2, dict)
    assert len(response2['animals']) == 150
    assert isinstance(response2_df, DataFrame)
    assert response2_df.shape[0] == 150

    assert isinstance(response3, dict)
    assert len(response3['animals']) == 3
    assert isinstance(response3_df, DataFrame)
    assert response3_df.shape[0] == 3

    assert isinstance(response4, dict)
    assert isinstance(response4['animals'], dict)
    assert isinstance(response4_df, DataFrame)
    assert response4_df.shape[0] == 1

    assert isinstance(response5, dict)
    assert isinstance(response5['animals'], list)

    assert isinstance(response6, dict)
    assert isinstance(response6['animals'], list)

    assert isinstance(response7, dict)
    assert isinstance(response7['animals'], list)

    assert isinstance(response8, dict)
    assert isinstance(response8['animals'], list)

    assert all(x == response9['environment.cats'][0] for x in response9['environment.cats'])
    assert all(x == response9['environment.children'][0] for x in response9['environment.children'])
    assert all(x == response9['environment.dogs'][0] for x in response9['environment.dogs'])

    assert all(x == response10['attributes.declawed'][0] for x in response10['attributes.declawed'])
    assert all(x == response10['attributes.house_trained'][0] for x in response10['attributes.house_trained'])
    assert all(x == response10['attributes.special_needs'][0] for x in response10['attributes.special_needs'])

    assert isinstance(response11['animals'], list)


@vcr.use_cassette('tests/cassettes/organizations.yml')
def test_organizations():
    response1 = pf.organizations()
    response1_df = pf.organizations(return_df=True)
    response2 = pf.organizations(results_per_page=50, pages=3)
    response2_df = pf.organizations(results_per_page=50, pages=3, return_df=True)

    org_ids = []
    for i in response1['organizations'][0:3]:
        org_ids.append(i['id'])
    
    response3 = pf.organizations(organization_id=org_ids)
    response3_df = pf.organizations(organization_id=org_ids, return_df=True)
    response4 = pf.organizations(organization_id=org_ids[0])
    response4_df = pf.organizations(organization_id=org_ids[0], return_df=True)

    assert isinstance(response1, dict)
    assert len(response1['organizations']) == 20
    assert isinstance(response1_df, DataFrame)

    assert isinstance(response2, dict)
    assert len(response2['organizations']) == 150
    assert isinstance(response2_df, DataFrame)
    assert response2_df.shape[0] == 150

    assert isinstance(response3, dict)
    assert len(response3['organizations']) == 3
    assert isinstance(response3_df, DataFrame)
    assert response3_df.shape[0] == 3

    assert isinstance(response4, dict)
    assert isinstance(response4['organizations'], dict)
    assert isinstance(response4_df, DataFrame)
    assert response4_df.shape[0] == 1


def test_check_parameters():
    size1, size2 = 'big', 'bigger'
    gender1, gender2 = 'MF', 'FM'
    age1, age2 = 'kitten', 'puppy'
    coat1, coat2 = 'fluffy', 'more fluffy'
    status = 'cute'
    sort = 'ascending'
    distance_int, distance_str = 1000, '1000'
    limit_int, limit_str = 200, '200'
    declawed = 'yes'
    house_trained = 'yes'
    special_needs = 'yes'
    good_with_children = 'yes'
    good_with_cats = 'yes'
    good_with_dogs = 'yes'

    with pytest.raises(ValueError):
        pf.animals(size=size1)
    with pytest.raises(ValueError):
        pf.animals(size=[size1, size2])
    with pytest.raises(ValueError):
        pf.animals(gender=gender1)
    with pytest.raises(ValueError):
        pf.animals(gender=[gender1, gender2])
    with pytest.raises(ValueError):
        pf.animals(age=age1)
    with pytest.raises(ValueError):
        pf.animals(age=[age1, age2])
    with pytest.raises(ValueError):
        pf.animals(coat=coat1)
    with pytest.raises(ValueError):
        pf.animals(coat=[coat1, coat2])
    with pytest.raises(ValueError):
        pf.animals(status=status)
    with pytest.raises(ValueError):
        pf.animals(sort=sort)
    with pytest.raises(ValueError):
        pf.animals(distance=distance_int)
    with pytest.raises(ValueError):
        pf.animals(distance=distance_str)
    with pytest.raises(ValueError):
        pf.animals(results_per_page=limit_int)
    with pytest.raises(ValueError):
        pf.animals(results_per_page=limit_str)
    with pytest.raises(ValueError):
        pf.animals(declawed=declawed)
    with pytest.raises(ValueError):
        pf.animals(house_trained=house_trained)
    with pytest.raises(ValueError):
        pf.animals(special_needs=special_needs)
    with pytest.raises(ValueError):
        pf.animals(good_with_cats=good_with_cats)
    with pytest.raises(ValueError):
        pf.animals(good_with_dogs=good_with_dogs)
    with pytest.raises(ValueError):
        pf.animals(good_with_children=good_with_children)
