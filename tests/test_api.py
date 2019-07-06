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


def authenticate():
    pf = Petfinder(str(key))

    return pf


pf = authenticate()
