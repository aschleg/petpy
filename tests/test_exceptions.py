import pytest
from petpy import Petfinder
from petpy.exceptions import PetfinderError, PetfinderInvalidCredentials, PetfinderInsufficientAccess, \
    PetfinderResourceNotFound
from tests.test_api import key, secret_key


def test_petfinder_invalidcredentials():
    test_key, test_secret = 'test', 'test1'

    with pytest.raises(PetfinderError):
        Petfinder(key=test_key, secret=test_secret)
    with pytest.raises(PetfinderInvalidCredentials):
        Petfinder(key=test_key, secret=test_secret)


def test_petfinder_insufficientaccess():
    p = Petfinder(key=key, secret=secret_key)

    p._host = 'http://api.petfinder.com/v3/'

    with pytest.raises(PetfinderInsufficientAccess):
        p.animal_types('cat')


def test_petfinder_resourcenotfound():
    p = Petfinder(key=key, secret=secret_key)
    with pytest.raises(PetfinderResourceNotFound):
        p.animals(animal_id=0)
